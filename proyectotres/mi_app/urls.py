from django.urls import path
from . import views
from .views import eliminar_persona, descargas, cargar_csv

urlpatterns = [
    path('formulario/', views.formulario, name='formulario'),  # La vista 'home' debe estar definida en views.py
    path('', views.hola_mundo, name='hola_mundo'),  # La vista 'home' debe estar definida en views.py
    path('eliminar-persona/<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
    path('descargas/', views.descargas, name='descargas'),
    path('atender-persona/<int:persona_id>/', views.atender_persona, name='atender_persona'),
    path('personas-atendidas/', views.personas_atendidas, name='personas_atendidas'),
    path('cargar-csv/', cargar_csv, name='cargar_csv'),
    # Puedes agregar más rutas aquí
]
