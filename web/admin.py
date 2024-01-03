from django.contrib import admin

# Register your models here.
from .models import Categoria, Producto

admin.site.register(Categoria)
#admin.site.register(Producto)

#uso de un decorador
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'fecha_registro')
    list_editable = ('precio',)