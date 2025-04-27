from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RolViewSet, UsuarioViewSet, CategoriaViewSet, VideojuegoViewSet, CompraViewSet, DetalleCompraViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'videojuegos', VideojuegoViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'detalles-compra', DetalleCompraViewSet)

#api/
urlpatterns = [
    path('categorias/', views.listar_categorias, name='listar_categorias'),
]
