from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def project_file_upload_to(instance, filename):
    # organiza por usuario y proyecto
    return f'projects/user_{instance.author.id}/{instance.title}/{filename}'

class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # permitimos múltiples archivos con modelo asociado
    def __str__(self):
        return f'{self.title} — {self.author}'

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=project_file_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return self.file.name.split('/')[-1]
