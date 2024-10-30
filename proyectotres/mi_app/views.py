# mi_app/views.py
import csv
from django.shortcuts import render, redirect, get_object_or_404
from .models import Persona  # Importar el modelo Persona
from django import forms
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt

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
        nombre = request.POST['nombre']  # Obtener el nombre del formulario
        apellido = request.POST['apellido']  # Obtener el apellido del formulario
        edad = request.POST['edad']  # Obtener la edad del formulario
        
        # Obtén el siguiente turno
        turno = Persona.objects.count() + 1  # Asigna el siguiente número de turno contando las personas

        nueva_persona = Persona(nombre=nombre, apellido=apellido, edad=edad, turno=turno)  # Crear una nueva instancia de Persona
        nueva_persona.save()  # Guardar la nueva persona en la base de datos
        
        return redirect('hola_mundo')  # Redirigir a la vista 'hola_mundo' después de guardar
    
    return render(request, 'mi_app/formulario.html')  # Renderizar el formulario si no es un POST

# Vista para eliminar una persona por ID
@csrf_exempt
def eliminar_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)  # Obtener la persona por ID o devolver un 404 si no existe
    persona.delete()  # Eliminar la persona
    return redirect('hola_mundo')  # Redirigir a la vista 'hola_mundo' después de eliminar


def atender_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)
    
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

    return render(request, 'mi_app/atender.html', {'persona': persona})

def personas_atendidas(request):
    atendidas = Persona.objects.filter(atendido=True)
    return render(request, 'mi_app/atendidos.html', {'personas_atendidas': atendidas})

# Vista para mostrar la página de descargas
def descargas(request):
    personas_atendidas = Persona.objects.filter(atendido=True) #Obtener las personas y filtrarlas a las que estan atendidas
    return render(request, 'mi_app/descargas.html', {'personas_atendidas': personas_atendidas}) #Renderizar las personas atendidas
def cargar_csv(request):
    mensaje = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['file']
            lector = csv.DictReader(archivo.read().decode('utf-8').splitlines())
            for fila in lector:
                Persona.objects.create(
                    nombre=fila['nombre'],
                    apellido=fila['apellido'],
                    edad=int(fila['edad']),
                    turno=int(fila['turno']),
                    atendido=bool(int(fila['atendido'])),
                    fecha_cita=fila['fecha_cita'] or None,
                    persona_encargada=fila['persona_encargada'] or None,
                )
            mensaje = 'CSV cargado con éxito.'
    else:
        form = UploadFileForm()
    return render(request, 'mi_app/cargar_csv.html', {'form': form, 'mensaje': mensaje})

