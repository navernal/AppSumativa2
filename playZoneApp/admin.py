from django.contrib import admin
from .models import Rol, Usuario, Categoria, Videojuego, Compra, DetalleCompra


class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'nombres', 'apellido_paterno','apellido_materno', 'correo', 'fecha_nacimiento', 'direccion_despacho', 'rol')
    search_fields = ('nombre_usuario', 'correo')
    list_filter = ('rol',)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'categoria')
    search_fields = ('nombre',)
    list_filter = ('categoria',)


class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_compra', 'total')
    search_fields = ('usuario__nombre_usuario',)
    list_filter = ('fecha_compra',)


class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'videojuego', 'cantidad', 'subtotal')
    search_fields = ('videojuego__nombre',)
    list_filter = ('videojuego',)


admin.site.register(Rol, RolAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Videojuego, VideojuegoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleCompra, DetalleCompraAdmin)
