from django.shortcuts import render
from playZoneApp.decorators import login_requerido
from django.shortcuts import render, redirect
from playZoneApp.backend import CustomAuthBackend 
from django.contrib import messages
from .models import Usuario,Categoria,Videojuego,Compra,DetalleCompra
from .forms import UsuarioForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings


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
    api_url = f'{settings.API_BASE_URL}categorias/'
    response = requests.get(api_url)

    if response.status_code == 200:
        categorias = response.json()
        for cat in categorias:
            cat["nombre"] = cat["nombre"].replace("_", "")
    else:
        categorias = []

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return redirect('login')
    
    return render(request, 'index.html', {'usuario': usuario, 'categorias': categorias})

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
    carrito = request.session.get('carrito', [])
    
    if not carrito:
        return redirect('carrito')  

    total = sum(item['precio'] for item in carrito)
    
    compra = Compra.objects.create(usuario=request.user, fecha_compra=timezone.now(), total=total)

    for item in carrito:
        videojuego = Videojuego.objects.get(nombre=item['nombre'])
        DetalleCompra.objects.create(compra=compra, videojuego=videojuego, cantidad=1, subtotal=item['precio'])
    request.session['carrito'] = []

    return render(request, 'pago.html', {'compra': compra})

def recuperar_contrasena(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["email"]
            try:
                usuario = User.objects.get(email=correo)
                send_mail(
                    'Recuperación de Contraseña',
                    'Aquí tienes el enlace para restablecer tu contraseña: <inserta_enlace_de_recuperación>',
                    'no-reply@virtualplayzone.com',
                    [correo],
                    fail_silently=False,
                )
                messages.success(request, "Te hemos enviado un enlace para restablecer tu contraseña.")
                return redirect('recuperar_contraseña') 
            except User.DoesNotExist:
                messages.error(request, "Este correo no está registrado.")
                return redirect('recuperar_contraseña')
    else:
        form = PasswordResetForm()

    return render(request, 'recuperar.html', {'form': form})

@login_requerido
def usuarios_admin(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios_admin.html', {'usuarios': usuarios})

@login_requerido
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado con éxito.")
            return redirect('usuarios_admin')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = UsuarioForm()

    return render(request, 'form_usuario.html', {'form': form, 'titulo': 'Crear Usuario'})

@login_requerido
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario_actual = Usuario.objects.get(id=request.session['user_id'])

    if usuario.fecha_nacimiento:
        usuario.fecha_nacimiento = usuario.fecha_nacimiento.strftime('%Y-%m-%d')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario, usuario_actual=usuario_actual)
        if form.is_valid():
            usuario_editado = form.save(commit=False)
            if not form.cleaned_data['clave']:
                usuario_editado.clave = usuario.clave 

            usuario_editado.save()
            if usuario_actual.rol.nombre == 'admin':
                messages.success(request, "Usuario actualizado con éxito.")
                return redirect('usuarios_admin')
            else:
                messages.success(request, "Perfil actualizado con éxito.")
                return redirect('index')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = UsuarioForm(instance=usuario, usuario_actual=usuario_actual)
        if not form.initial.get('fecha_nacimiento'):
            form.initial['fecha_nacimiento'] = usuario.fecha_nacimiento

    return render(request, 'form_usuario.html', {
        'form': form,
        'titulo': 'Editar Usuario' if usuario_actual.rol.nombre == 'admin' else 'Editar Perfil',
        'usuario_actual': usuario_actual
    })

@login_requerido
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios_admin')
    return render(request, 'confirmar_eliminacion.html', {'usuario': usuario})


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    
    logout(request)

    return redirect('login')  

def juegos_por_categoria(request, categoria_id):
    api_url = f'{settings.API_BASE_URL}videojuegos/categoria/{categoria_id}/'

    response = requests.get(api_url)    
    if response.status_code == 200:
        data = response.json()
        nombre_categoria = data.get("nombre_categoria", "Desconocida")  
        juegos = data.get("videojuegos", [])  
    else:
        juegos = []
        nombre_categoria = "Categoría no encontrada"

    return render(request, 'juegos_por_categoria.html', {
        'juegos': juegos,
        'nombre_categoria': nombre_categoria
    })
    
@login_requerido
def actualizar_carrito(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['carrito'] = data['carrito']
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_requerido
def lista_pokemon(request):
    response = requests.get(settings.API_POKE+'pokemon?limit=20')
    pokemons = []

    if response.status_code == 200:
        data = response.json()
        for item in data['results']:
            detail = requests.get(item['url']).json()
            pokemon = {
                'name': item['name'],
                'image': detail['sprites']['front_default'],
                'height': detail['height'],
                'weight': detail['weight'],
                'types': [t['type']['name'] for t in detail['types']]
            }
            pokemons.append(pokemon)

    return render(request, 'pokemon_template.html', {'pokemons': pokemons})

@login_requerido
def lista_rickmorty(request):
    response = requests.get(settings.API_RICK + 'character')
    if response.status_code == 200:
        data = response.json()
        characters = data['results']
    else:
        characters = []
    return render(request, 'rick_template.html', {'characters': characters})

@csrf_exempt
def registrar_pago(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        total = data.get("total")
        carrito = data.get("carrito", [])
        
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({"error": "Usuario no autenticado"}, status=401)

        usuario = Usuario.objects.get(id=user_id)
        compra = Compra.objects.create(usuario=usuario, total=total)
        for item in carrito:
            videojuego = Videojuego.objects.get(nombre=item["nombre"])  
            cantidad = 1  
            subtotal = videojuego.precio * cantidad 

            DetalleCompra.objects.create(
                compra=compra,
                videojuego=videojuego,
                cantidad=cantidad,
                subtotal=subtotal
            )

        return JsonResponse({"status": "ok", "compra_id": compra.id})
    return JsonResponse({"error": "Método no permitido"}, status=405)
