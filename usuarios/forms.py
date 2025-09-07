from django import forms
from django.contrib.auth.models import User
from .models import Empresa

class RegistroEmpresaForm(forms.ModelForm):
    nombre_empresa = forms.CharField(max_length=255, label="Nombre de la empresa")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Empresa.objects.create(usuario=user, nombre=self.cleaned_data['nombre_empresa'])
        return user
