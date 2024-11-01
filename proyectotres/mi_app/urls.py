from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import eliminar_persona, cargar_archivo, descargar_csv, descargar_pdf, descargas, descargar_csv_completo, descargar_pdf_completo

urlpatterns = [
    path('', views.hola_mundo, name='hola_mundo'),  # La vista 'home' debe estar definida en views.py
    path('formulario/', views.formulario, name='formulario'),
    path('eliminar-persona/<int:persona_id>/', eliminar_persona, name='eliminar_persona'),
    path('descargas/', descargas, name='descargas'),
    path('descargar-csv/', descargar_csv, name='descargar_csv'),
    path('descargar-csv-completo/', descargar_csv_completo, name='descargar_csv_completo'),
    path('descargar-pdf/', descargar_pdf, name='descargar_pdf'),
    path('descargar-pdf-completo/', descargar_pdf_completo, name='descargar_pdf_completo'),
    path('atender-persona/<int:persona_id>/', views.atender_persona, name='atender_persona'),
    path('personas-atendidas/', views.personas_atendidas, name='personas_atendidas'),
    path('cargar-csv/', cargar_archivo, name='cargar_csv'),
    # Puedes agregar más rutas aquí
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)