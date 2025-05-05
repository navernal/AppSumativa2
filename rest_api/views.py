from django.shortcuts import render
from rest_framework import viewsets
from playZoneApp.models import Rol, Usuario, Categoria, Videojuego, Compra, DetalleCompra
from .serializers import CategoriaSerializer, VideojuegoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class VideojuegoViewSet(viewsets.ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializer
    
    @action(detail=False, methods=['get'], url_path='categoria/(?P<categoria_id>\d+)')
    def por_categoria(self, request, categoria_id=None):
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            juegos = Videojuego.objects.filter(categoria=categoria)
            serializer = self.get_serializer(juegos, many=True)
            
            response_data = {
                "nombre_categoria": categoria.nombre,
                "videojuegos": serializer.data
            }
            
            return Response(response_data)
            
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=404)

