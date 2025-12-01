from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Project, ProjectFile

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo o usuario')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_url']

class ProjectFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def clean_files(self):
        files = self.files.getlist('files') if hasattr(self, 'files') else []
        # Validar tipos permitidos
        allowed_ext = ['.txt', '.docx', '.xlsx']
        for f in files:
            name = f.name.lower()
            if not any(name.endswith(ext) for ext in allowed_ext):
                raise forms.ValidationError(f'Archivo {f.name} no permitido. Tipos permitidos: {", ".join(allowed_ext)}')
            if f.size > 5 * 1024 * 1024:  # 5 MB por archivo (ajusta si quieres)
                raise forms.ValidationError(f'Archivo {f.name} excede 5MB.')
        return files
