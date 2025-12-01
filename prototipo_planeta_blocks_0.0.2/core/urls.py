from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrarse/', views.register_view, name='register'),
    path('iniciar-sesion/', views.login_view, name='login'),
    path('cerrar-sesion/', views.logout_view, name='logout'),
    path('subir/', views.upload_project_view, name='upload_project'),
    path('mis-proyectos/', views.my_projects, name='my_projects'),
    path('proyecto/<int:pk>/', views.project_detail, name='project_detail'),
]
