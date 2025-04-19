from django.db import models

# Create your models here.
class Sexo(models.Model):
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.description
    
    
class Carerra(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
