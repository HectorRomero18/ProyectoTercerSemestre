from django.contrib import admin
from .models import Persona

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'edad')  # Campos que se mostrarán en la lista
    search_fields = ('nombre', 'apellido')  # Campos que se pueden buscar

