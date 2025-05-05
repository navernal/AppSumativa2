from django.db import models
from django.contrib.auth.hashers import check_password

# Create your models here.
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    nombres= models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno= models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(unique=True)
    clave = models.CharField(max_length=128)  
    fecha_nacimiento = models.DateField()
    direccion_despacho = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)


    def __str__(self):
        return self.nombre_usuario
    
    
    def verificar_clave(self, password):
        return password == self.clave

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.videojuego.nombre} x{self.cantidad} (Compra #{self.compra.id})"