from django.shortcuts import render
from playZoneApp.decorators import login_requerido
from django.shortcuts import render, redirect
from playZoneApp.backend import CustomAuthBackend 
from django.contrib import messages
from .models import Usuario



# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['contrasena']
        custom_auth_backend = CustomAuthBackend()
        user = custom_auth_backend.authenticate(request, username=username, password=password)
        print(f"usuario: {user.rol}")
        if user is not None:
            request.session['user_id'] = user.id  
            return redirect('index') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')

@login_requerido
def index(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return redirect('login')
    return render(request, 'index.html', {'usuario': usuario})

@login_requerido
def Accion(request):
    return render(request, 'Accion.html')

@login_requerido
def Carreras(request):
    return render(request, 'Carreras.html')

@login_requerido
def FreeToPlay(request):
    return render(request, 'FreeToPlay.html')

@login_requerido
def MundoAbierto(request):
    return render(request, 'MundoAbierto.html')

@login_requerido
def Supervivencia(request):
    return render(request, 'Supervivencia.html')

@login_requerido
def Terror(request):
    return render(request, 'Terror.html')

@login_requerido
def RegistrarUsuario(request):
    return render(request, 'Registrodeusuario.html')

@login_requerido
def foro(request):
    return render(request, 'foro.html')

@login_requerido
def carrito(request):
    return render(request, 'carrito.html')

@login_requerido
def pago(request):
    return render(request, 'pago.html')

@login_requerido
def recuperar(request):
    return render(request, 'recuperar.html')

