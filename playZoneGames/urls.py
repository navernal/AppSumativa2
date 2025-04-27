"""
URL configuration for playZoneGames project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from playZoneApp import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('Accion/', views.Accion, name='Accion'),
    path('Carreras/', views.Carreras, name='Carreras'),
    path('FreeToPlay/', views.FreeToPlay, name='FreeToPlay'),
    path('MundoAbierto/', views.MundoAbierto, name='MundoAbierto'),
    path('Supervivencia/', views.Supervivencia, name='Supervivencia'),
    path('Terror/', views.Terror, name='Terror'),
    path('registroUsuario/', views.RegistrarUsuario, name='RegistroUsuario'),  
    path('foro/', views.foro, name='foro'),
    path('carrito/', views.carrito, name='carrito'),
    path('pago/', views.pago, name='pago'),
    path('recuperar/', views.recuperar_contrasena, name='recuperar'),
    path('usuarios/', views.usuarios_admin, name='usuarios_admin'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('categoria/<int:categoria_id>/', views.juegos_por_categoria, name='juegos_por_categoria'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('registrar_pago/', views.registrar_pago, name='registrar_pago'),
    path('api/', include('rest_api.urls')),


]
