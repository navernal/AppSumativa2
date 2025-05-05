from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from playZoneApp.models import Usuario  # Asegúrate de usar el modelo correcto


class CustomAuthBackend():
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuario.objects.get(nombre_usuario=username)
            if usuario.verificar_clave(password):
                return usuario
        except Usuario.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None

