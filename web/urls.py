from django.urls import path

from . import views

app_name = 'web'
 
urlpatterns = [
    path('', views.index,name = 'index'),
    path('productosPorCategoria/<int:categoria_id>', views.productosPorCategoria, name = 'productosPorCategoria'),
    path('productosPorNombre', views.productosPorNombre, name = 'productosPorNombre' ),
    path('producto/<int:producto_id>', views.productoDetalle, name = 'producto'),
    path('carrito',views.carrito,name='carrito'),
    path('agregarCarrito/<int:producto_id>', views.agregarCarrito,name='agregarCarrito'),
    path('eliminarProductoCarrito/<int:producto_id>', views.eliminarProductoCarrito,name='eliminarProductoCarrito'),
    path('limpiarCarrito', views.limpiarCarrito,name='limpiarCarrito')

    
]
