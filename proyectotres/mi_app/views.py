# mi_app/views.py
import csv
import pdfplumber
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona  # Importar el modelo Persona
from django import forms
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Vista para mostrar un saludo y la lista de personas
def hola_mundo(request):
    personas = Persona.objects.all()
    atendidos = [persona for persona in personas if persona.atendido]
    
    return render(request, 'hola_mundo.html', {
        'personas': personas,
        'atendidos': atendidos,  # Pasar lista de atendidos
    })

# Vista para manejar el formulario de registro de personas
def formulario(request):
    if request.method == 'POST':  # Si se envía el formulario
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        edad = request.POST['edad']
        
        # Obtén el siguiente turno
        turno = Persona.objects.count() + 1

        try:
            # Verificar que no esté vacío y que se pueda convertir a entero
            if nombre and apellido and edad:
                # Verificar si la persona ya existe
                if not Persona.objects.filter(nombre=nombre, apellido=apellido, edad=int(edad)).exists():
                    nueva_persona = Persona(nombre=nombre, apellido=apellido, edad=int(edad), turno=turno)  # Asegúrate de convertir edad a int
                    nueva_persona.save()  # Guardar la nueva persona en la base de datos
                    return redirect('hola_mundo')  # Redirigir a la vista 'hola_mundo' después de guardar
                else:
                    return render(request, 'mi_app/formulario.html', {
                        'error': "Esta persona ya está registrada."
                    })
        
        except Exception as e:
            print(f"Error al guardar a la persona: {e}")
            return render(request, 'mi_app/formulario.html', {
                'error': "Hubo un error al guardar a la persona. Inténtalo de nuevo."
            })

    return render(request, 'mi_app/formulario.html')  # Renderizar el formulario si no es un POST

# Vista para eliminar una persona por ID
@csrf_exempt
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)  # Obtener la persona por ID o devolver un 404 si no existe
    persona.delete()  # Eliminar la persona
    return redirect('hola_mundo')  # Redirigir a la vista 'hola_mundo' después de eliminar


def atender_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    try:
        if request.method == 'POST':
            # Aquí obtienes los datos del formulario, como fecha de cita y persona encargada
            fecha_cita = request.POST['fecha_cita']
            persona_encargada = request.POST['persona_encargada']

            # Guardar los datos en la persona
            persona.fecha_cita = fecha_cita
            persona.persona_encargada = persona_encargada
            persona.atendido = True  # Asigna el estado de atendido
            
            persona.save()  # Guarda los cambios en la base de datos
            
            return redirect('hola_mundo')  # Redirige a hola_mundo
    except Exception as e:
        print(f"Ocurrio un error al atender a la persona: {e}")
        return render(request, 'mi_app/atender.html') 
    return render(request, 'mi_app/atender.html')

def personas_atendidas(request):
    atendidas = Persona.objects.filter(atendido=True)
    return render(request, 'mi_app/atendidos.html', {'personas_atendidas': atendidas})

# Vista para mostrar la página de descargas
def descargas(request):
    personas_atendidas = Persona.objects.filter(atendido=True)
    return render(request, 'mi_app/descargas.html', {'personas_atendidas': personas_atendidas})

def descargar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=personas_atendidas.csv'
    
    writer = csv.writer(response)
    writer.writerow(['nombre', 'apellido', 'edad', 'turno', 'atendido', 'fecha_cita', 'persona_encargada'])  # Encabezados

    personas_atendidas = Persona.objects.filter(atendido=True)
    
    for persona in personas_atendidas:
        writer.writerow([
            persona.nombre,
            persona.apellido,
            persona.edad,
            persona.turno,
            persona.atendido,
            persona.fecha_cita,
            persona.persona_encargada
        ])

    return response


def descargar_pdf_completo(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="todas_personas.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezados
    p.drawString(100, height - 50, "Nombre")
    p.drawString(200, height - 50, "Apellido")
    p.drawString(300, height - 50, "Edad")
    p.drawString(400, height - 50, "Turno")
    p.drawString(500, height - 50, "Atendido")
    p.drawString(600, height - 50, "Fecha Cita")
    p.drawString(700, height - 50, "Persona Encargada")

    todas_personas = Persona.objects.all()

    y = height - 70
    for persona in todas_personas:
        p.drawString(100, y, persona.nombre)
        p.drawString(200, y, persona.apellido)
        p.drawString(300, y, str(persona.edad))
        p.drawString(400, y, str(persona.turno))
        p.drawString(500, y, str(persona.atendido))
        
        # Convertir la fecha a string si no es None
        fecha_cita = persona.fecha_cita.strftime('%Y-%m-%d') if persona.fecha_cita else ""
        p.drawString(600, y, fecha_cita)
        
        persona_encargada = persona.persona_encargada or ""
        p.drawString(700, y, persona_encargada)
        y -= 20  # Espaciado entre filas

    p.showPage()
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response



def descargar_csv_completo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="todas_personas.csv"'

    writer = csv.writer(response)
    writer.writerow(['nombre', 'apellido', 'edad', 'turno', 'atendido', 'fecha_cita', 'persona_encargada'])  # Encabezados

    todas_personas = Persona.objects.all()  # Obtener todas las personas
    
    for persona in todas_personas:
        writer.writerow([
            persona.nombre,
            persona.apellido,
            persona.edad,
            persona.turno,
            persona.atendido,
            persona.fecha_cita,
            persona.persona_encargada
        ])

    return response

def descargar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=personas_atendidas.pdf'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Encabezados
    p.drawString(100, height - 50, "Nombre")
    p.drawString(200, height - 50, "Apellido")
    p.drawString(300, height - 50, "Edad")
    p.drawString(400, height - 50, "Turno")
    p.drawString(500, height - 50, "Atendido")
    p.drawString(600, height - 50, "Fecha Cita")
    p.drawString(700, height - 50, "Persona Encargada")

    personas_atendidas = Persona.objects.filter(atendido=True)

    y = height - 70
    for persona in personas_atendidas:
        p.drawString(100, y, persona.nombre)
        p.drawString(200, y, persona.apellido)
        p.drawString(300, y, str(persona.edad))
        p.drawString(400, y, str(persona.turno))
        p.drawString(500, y, str(persona.atendido))
        
        # Convertir la fecha a string si no es None
        fecha_cita = persona.fecha_cita.strftime('%Y-%m-%d') if persona.fecha_cita else ""
        p.drawString(600, y, fecha_cita)
        
        persona_encargada = persona.persona_encargada or ""
        p.drawString(700, y, persona_encargada)
        y -= 20  # Espaciado entre filas

    p.showPage()
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response


from django.shortcuts import redirect, render
from django.contrib import messages
import csv

def cargar_archivo(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['file']

            if archivo.name.endswith('.csv'):
                # Procesar CSV
                try:
                    lector = csv.DictReader(archivo.read().decode('utf-8').splitlines())
                    expected_fields = ['turno', 'nombre', 'apellido', 'edad']

                    if not all(field in lector.fieldnames for field in expected_fields):
                        raise ValueError("El archivo CSV no contiene todos los campos necesarios.")

                    for fila in lector:
                        print(f"Datos a crear: {fila}")  # Imprimir los datos leídos
                        Persona.objects.create(
                            turno=int(fila['turno']),
                            nombre=fila['nombre'],
                            apellido=fila['apellido'],
                            edad=int(fila['edad']),
                            atendido=fila['atendido'].lower() == 'true', 
                        )
                    messages.success(request, 'CSV cargado con éxito.')
                    
                    # Redirigir a la pantalla principal
                    return redirect('hola_mundo')  # Cambia 'hola_mundo' por el nombre de tu vista correspondiente

                except Exception as e:
                    messages.error(request, f'Error al procesar el CSV: {e}')
                    # Si ocurre un error, puedes optar por permanecer en la misma página
                    # return render(request, 'mi_app/cargar_archivo.html', {'form': form})

    else:
        form = UploadFileForm()

    return render(request, 'mi_app/cargar_archivo.html', {'form': form})
