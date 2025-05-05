from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, VideojuegoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'videojuegos', VideojuegoViewSet, basename='videojuego')

urlpatterns = [
    path('', include(router.urls)),
]