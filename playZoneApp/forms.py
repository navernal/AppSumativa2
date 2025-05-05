from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellido_paterno', 'apellido_materno', 'nombre_usuario', 'correo', 'clave', 'fecha_nacimiento', 'direccion_despacho', 'rol']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'clave': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion_despacho': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)

        self.fields['clave'].required = False

        if self.usuario_actual and self.usuario_actual.rol.nombre == 'public':
            self.fields['rol'].disabled = True

    def clean_clave(self):
        clave = self.cleaned_data.get('clave')

        if clave and len(clave) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if clave and len(clave) > 20:
            raise ValidationError("La contraseña no puede tener más de 20 caracteres.")

        if clave and not re.search(r'[!@#$%^&*(),.?":{}|<>]', clave):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")

        if clave and (not re.search(r'[A-Za-z]', clave) or not re.search(r'[0-9]', clave)):
            raise ValidationError("La contraseña debe contener al menos una letra y un número.")

        nombre_usuario = self.cleaned_data.get('nombre_usuario')
        if nombre_usuario and nombre_usuario.lower() in clave.lower():
            raise ValidationError("La contraseña no puede contener el nombre de usuario.")

        return clave
