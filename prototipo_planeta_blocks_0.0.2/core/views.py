from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProjectForm, ProjectFileForm
from .models import Project, ProjectFile

def index(request):
    projects = Project.objects.select_related('author').order_by('-created_at')[:12]
    return render(request, 'core/index.html', {'projects': projects})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente. ¡Bienvenido!')
            return redirect('core:index')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente.')
            return redirect('core:index')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada.')
    return redirect('core:index')

@login_required
def upload_project_view(request):
    if request.method == 'POST':
        pform = ProjectForm(request.POST)
        files = request.FILES.getlist('files')
        if pform.is_valid():
            project = pform.save(commit=False)
            project.author = request.user
            project.save()

            for f in files:
                pf = ProjectFile(project=project, file=f)
                pf.save()

            messages.success(request, 'Proyecto subido con éxito (modo real).')
            return redirect('core:project_detail', pk=project.pk)
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        pform = ProjectForm()
    return render(request, 'core/upload_project.html', {'form': pform})

@login_required
def my_projects(request):
    projs = Project.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'core/my_projects.html', {'projects': projs})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    files = project.files.all()
    return render(request, 'core/project_detail.html', {'project': project, 'files': files})
