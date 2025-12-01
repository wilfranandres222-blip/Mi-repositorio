from django.contrib import admin
from .models import Project, ProjectFile

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    inlines = [ProjectFileInline]
