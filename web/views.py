from django.shortcuts import render,get_object_or_404,redirect

from django.urls import reverse

from .models import Categoria,Producto,Cliente,Pedido,PedidoDetalle

#from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
""" VISTAS PARA EL CATALOGO DE PRODUCTOS """

def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    
    #print(listaProductos)
    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }
    return render(request,'index.html',context)

def productosPorCategoria(request,categoria_id):
    """ vista para filtrar productos por categoria """
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()
    
    listaCategorias = Categoria.objects.all()
    
    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }
    
    return render(request,'index.html',context)

def productosPorNombre(request):
    """ vista para filtrado de productos por nombre """
    nombre = request.POST['nombre']
    
    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()
    
    context = {
        'categorias':listaCategorias,
        'productos':listaProductos
    }
    
    return render(request,'index.html',context)

def productoDetalle(request,producto_id):
    """ vista para el detalle de producto"""
    
    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto,pk=producto_id)
    context = {
        'producto':objProducto
    }
    
    return render(request,'producto.html',context)

""" VISTAS PARA EL CARRITO DE COMPRAS """

from .carrito import Cart

def carrito(request):
    return render(request,'carrito.html')

def agregarCarrito(request,producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
    
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto,cantidad)
    
    #print(request.session.get("cart"))
    
    if request.method == 'GET':
        return redirect('/')
    
    return render(request,'carrito.html')

def eliminarProductoCarrito(request,producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)
    
    return render(request,'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()
    
    return render(request,'carrito.html')


""" VISTAS PARA CLIENTES Y USUARIOS """
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


from .forms import ClienteForm

def crearUsuario(request):
    
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']
        
        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect('/cuenta')
    
    
    return render(request,'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    context = {
        'destino':paginaDestino
    }
    
    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']
        
        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)
            
            if dataDestino != 'None':
                return redirect(dataDestino)
            
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos incorrectos'
            }
    
    return render(request,'login.html',context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')

def cuentaUsuario(request):
    
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
         }
    
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'cuenta.html',context)

def actualizarCliente(request):
    mensaje = ""
    
    if request.method == "POST":
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data
            
            #actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente["nombre"]
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            actUsuario.save()
            
            #registrar Cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = dataCliente["dni"]
            nuevoCliente.direccion = dataCliente["direccion"]
            nuevoCliente.telefono = dataCliente["telefono"]
            nuevoCliente.sexo = dataCliente["sexo"]
            nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            nuevoCliente.save()
            
            mensaje = "Datos Actualizados"
            
    context ={
        'mensaje':mensaje,
        'frmCliente':frmCliente
    }
            
    
    return render(request,'cuenta.html',context)

""" VISTAS PARA PROCESO DE COMPRA """

@login_required(login_url='/login')
def registrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)
        
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion':clienteEditar.direccion,
            'telefono':clienteEditar.telefono,
            'dni':clienteEditar.dni,
            'sexo':clienteEditar.sexo,
            'fecha_nacimiento':clienteEditar.fecha_nacimiento
        }
    except:
         dataCliente = {
            'nombre':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email
         }
    
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente':frmCliente
    }
    
    return render(request,'pedido.html',context)

@login_required(login_url='/login')
def registrarCompra(request):
    context = {}
    if request.method == "POST":
        print("motodo post")
        #registrar o actualizar el cliente
        frmCliente = ClienteForm(request.POST)
        #if frmCliente.is_valid():
        #print("datos de cliente validados")
        dataCliente = frmCliente.cleaned_data
            
        #actualizar usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name = dataCliente["nombre"]
        actUsuario.last_name = dataCliente["apellidos"]
        actUsuario.save()
            
        try:
            clientePedido = Cliente.objects.get(usuario = request.user)
            clientePedido.telefono = dataCliente["telefono"]
            clientePedido.direccion = dataCliente["direccion"]
            clientePedido.save()
        except:
            clientePedido = Cliente()
            clientePedido.usuario = actUsuario
            clientePedido.direccion = dataCliente["direccion"]
            clientePedido.telefono = dataCliente["telefono"]
            clientePedido.save()
            
        #registrar pedido
        nroPedido = ''
        montoTotal = 0
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()
        
        #registrar Detalle de Pedido
        carritoPedido = request.session.get('cart')
        for key,value in carritoPedido.items():
                
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            nuevoPedidoDetalle = PedidoDetalle()
            nuevoPedidoDetalle.pedido = nuevoPedido
            nuevoPedidoDetalle.producto = productoPedido
            nuevoPedidoDetalle.cantidad = int(value['cantidad'])
            nuevoPedidoDetalle.subtotal = float(value['subtotal'])
            nuevoPedidoDetalle.save()
            montoTotal += float(value['subtotal'])
            
        carrito = Cart(request)
        carrito.clear()
        
        #actualizar pedido
        nroPedido = 'PED' + nuevoPedido.fecha_registro.strtime('%Y') + str(nuevoPedido.id)
        nuevoPedido.nro_pedido = nroPedido
        nuevoPedido.monto_total = montoTotal
        nuevoPedido.save()
        
        #CREAMOS EL BOTON DE PAYPAL
        request.session['paypal_pid'] = nuevoPedido.id
            
        paypal_dict = {
            "business": "sb-mvtyu25103667@business.example.com",
            "amount": montoTotal,
            "item_name": "PEDIDO NRO : " + nroPedido,
            "invoice": nroPedido,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri('/confirmacion'),
            "cancel_return": request.build_absolute_uri('/')
        }

        # Create the instance.
        formPedidoPaypal = PayPalPaymentsForm(initial=paypal_dict)
            
        context = {
            'pedido':nuevoPedido,
            'formpaypal':formPedidoPaypal
        }
        
    return render(request,'compra.html',context)

def confirmacionPedido(request):
    return render(request,'gracias.html')

#prueba de paypal


def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-mvtyu25103667@business.example.com",
        "amount": "100.00",
        "item_name": "producto de prueba edteam",
        "invoice": "100-ED100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)
    
