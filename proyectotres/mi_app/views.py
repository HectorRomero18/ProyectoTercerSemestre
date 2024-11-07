# mi_app/views.py
import csv  # Módulo para trabajar con archivos CSV
import pdfplumber  # Módulo para trabajar con PDFs
from django.contrib import messages  # Para mostrar mensajes en la interfaz
from django.shortcuts import render, redirect, get_object_or_404  # Funciones para manejar vistas
from .models import Persona  # Importar el modelo Persona
from .metodos import ListaEnlazada
from django import forms  # Para formularios de Django
from .forms import UploadFileForm  # Importar el formulario para cargar archivos
from django.views.decorators.csrf import csrf_exempt  # Para manejar CSRF en vistas
from django.http import HttpResponse  # Para devolver respuestas HTTP
from io import BytesIO  # Para trabajar con flujos de bytes
from reportlab.lib.pagesizes import letter  # Para definir el tamaño de la página en PDF
from reportlab.pdfgen import canvas  # Para generar PDF

# Vista para mostrar un saludo y la lista de personas
def hola_mundo(request):
    personas = Persona.objects.all()  # Obtener todas las personas
    atendidos = [persona for persona in personas if persona.atendido]  # Filtrar las personas atendidas
    
    return render(request, 'hola_mundo.html', {
        'personas': personas,  # Pasar todas las personas a la plantilla
        'atendidos': atendidos,  # Pasar lista de atendidos a la plantilla
    })

# Vista para manejar el formulario de registro de personas
def formulario(request):
    if request.method == 'POST':  # Si se envía el formulario
        nombre = request.POST['nombre']  # Obtener el nombre del formulario
        apellido = request.POST['apellido']  # Obtener el apellido
        edad = request.POST['edad']  # Obtener la edad
        
        # Obtén el siguiente turno
        turno = Persona.objects.count() + 1  # Contar personas para asignar turno

        try:
            # Verificar que no esté vacío y que se pueda convertir a entero
            if nombre and apellido and edad:
                # Verificar si la persona ya existe
                if not Persona.objects.filter(nombre=nombre, apellido=apellido, edad=int(edad)).exists():
                    # Crear y guardar nueva persona
                    nueva_persona = Persona(nombre=nombre, apellido=apellido, edad=int(edad), turno=turno)
                    nueva_persona.save()  # Guardar la nueva persona en la base de datos
                    return redirect('hola_mundo')  # Redirigir a la vista 'hola_mundo' después de guardar
                else:
                    return render(request, 'mi_app/formulario.html', {
                        'error': "Esta persona ya está registrada."
                    })
        
        except Exception as e:
            print(f"Error al guardar a la persona: {e}")  # Imprimir error en la consola
            return render(request, 'mi_app/formulario.html', {
                'error': "Hubo un error al guardar a la persona. Inténtalo de nuevo."
            })

    return render(request, 'mi_app/formulario.html')  # Renderizar el formulario si no es un POST

# Vista para eliminar una persona por ID
@csrf_exempt  # Permitir solicitudes sin CSRF
def eliminar_persona(request, persona_id):
    # Obtener la persona a eliminar
    persona = get_object_or_404(Persona, id=persona_id)
    
    # Eliminar la persona de la base de datos
    persona.delete()
    
    # Reajustar los turnos de las personas restantes
    personas_restantes = Persona.objects.all().order_by('turno')  # Ordenar por turno
    
    # Asignar nuevos turnos secuenciales
    for index, persona in enumerate(personas_restantes, start=1):
        persona.turno = index  # Asignar el nuevo turno
        persona.save()  # Guardar el cambio en la base de datos
    
    # Redirigir a la vista principal
    return redirect('hola_mundo')


# Vista para atender a una persona
def atender_persona(request, persona_id):
    persona = get_object_or_404(Persona, id=persona_id)  # Obtener persona por ID
    try:
        if request.method == 'POST':  # Si se envía el formulario para atender
            # Obtener datos del formulario
            fecha_cita = request.POST['fecha_cita']
            persona_encargada = request.POST['persona_encargada']

            # Guardar los datos en la persona
            persona.fecha_cita = fecha_cita
            persona.persona_encargada = persona_encargada
            persona.atendido = True  # Asignar el estado de atendido
            
            persona.save()  # Guardar cambios en la base de datos
            
            return redirect('hola_mundo')  # Redirigir a hola_mundo
    except Exception as e:
        print(f"Ocurrio un error al atender a la persona: {e}")  # Imprimir error en la consola
        return render(request, 'mi_app/atender.html')  # Renderizar la página de atender

    return render(request, 'mi_app/atender.html', {'persona': persona} )  # Renderizar si no es un POST

# Vista para mostrar las personas atendidas
def personas_atendidas(request):
    atendidas = Persona.objects.filter(atendido=True)  # Filtrar personas atendidas
    return render(request, 'mi_app/atendidos.html', {'personas_atendidas': atendidas})  # Renderizar la plantilla

# Vista para mostrar la página de descargas
def descargas(request):
    personas_atendidas = Persona.objects.filter(atendido=True)  # Filtrar personas atendidas
    return render(request, 'mi_app/descargas.html', {'personas_atendidas': personas_atendidas})  # Renderizar la plantilla

# Vista para descargar CSV de personas atendidas
def descargar_csv(request):
    response = HttpResponse(content_type='text/csv')  # Establecer tipo de contenido para CSV
    response['Content-Disposition'] = 'attachment; filename=personas_atendidas.csv'  # Indicar nombre del archivo
    
    writer = csv.writer(response)  # Crear un escritor CSV
    writer.writerow(['nombre', 'apellido', 'edad', 'turno', 'atendido', 'fecha_cita', 'persona_encargada'])  # Encabezados

    personas_atendidas = Persona.objects.filter(atendido=True)  # Filtrar personas atendidas
    
    for persona in personas_atendidas:
        writer.writerow([  # Escribir cada persona en el CSV
            persona.nombre,
            persona.apellido,
            persona.edad,
            persona.turno,
            persona.atendido,
            persona.fecha_cita,
            persona.persona_encargada
        ])

    return response  # Devolver el archivo CSV

# Vista para descargar PDF completo de todas las personas
def descargar_pdf_completo(request):
    response = HttpResponse(content_type='application/pdf')  # Establecer tipo de contenido para PDF
    response['Content-Disposition'] = 'attachment; filename="todas_personas.pdf"'  # Indicar nombre del archivo

    buffer = BytesIO()  # Crear un buffer para el PDF
    p = canvas.Canvas(buffer, pagesize=letter)  # Crear un objeto de canvas para el PDF
    width, height = letter  # Definir tamaño de página

    # Encabezados en el PDF
    p.drawString(100, height - 50, "Nombre")
    p.drawString(200, height - 50, "Apellido")
    p.drawString(300, height - 50, "Edad")
    p.drawString(400, height - 50, "Turno")
    p.drawString(500, height - 50, "Atendido")
    p.drawString(600, height - 50, "Fecha Cita")
    p.drawString(700, height - 50, "Persona Encargada")

    todas_personas = Persona.objects.all()  # Obtener todas las personas

    y = height - 70  # Posición inicial en Y
    for persona in todas_personas:
        # Escribir cada persona en el PDF
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

    p.showPage()  # Finalizar la página
    p.save()  # Guardar el PDF
    buffer.seek(0)  # Reiniciar el buffer
    response.write(buffer.getvalue())  # Escribir contenido al response
    return response  # Devolver el PDF

# Vista para descargar CSV completo de todas las personas
def descargar_csv_completo(request):
    response = HttpResponse(content_type='text/csv')  # Establecer tipo de contenido para CSV
    response['Content-Disposition'] = 'attachment; filename="todas_personas.csv"'  # Indicar nombre del archivo

    writer = csv.writer(response)  # Crear un escritor CSV
    writer.writerow(['nombre', 'apellido', 'edad', 'turno', 'atendido', 'fecha_cita', 'persona_encargada'])  # Encabezados

    todas_personas = Persona.objects.all()  # Obtener todas las personas
    
    for persona in todas_personas:
        writer.writerow([  # Escribir cada persona en el CSV
            persona.nombre,
            persona.apellido,
            persona.edad,
            persona.turno,
            persona.atendido,
            persona.fecha_cita,
            persona.persona_encargada
        ])

    return response  # Devolver el archivo CSV

# Vista para descargar PDF de personas atendidas
def descargar_pdf(request):
    response = HttpResponse(content_type='application/pdf')  # Establecer tipo de contenido para PDF
    response['Content-Disposition'] = 'attachment; filename=personas_atendidas.pdf'  # Indicar nombre del archivo
    
    buffer = BytesIO()  # Crear un buffer para el PDF
    p = canvas.Canvas(buffer, pagesize=letter)  # Crear un objeto de canvas para el PDF
    width, height = letter  # Definir tamaño de página

    # Encabezados en el PDF
    p.drawString(100, height - 50, "Nombre")
    p.drawString(200, height - 50, "Apellido")
    p.drawString(300, height - 50, "Edad")
    p.drawString(400, height - 50, "Turno")
    p.drawString(500, height - 50, "Atendido")
    p.drawString(600, height - 50, "Fecha Cita")
    p.drawString(700, height - 50, "Persona Encargada")

    personas_atendidas = Persona.objects.filter(atendido=True)  # Filtrar personas atendidas

    y = height - 70  # Posición inicial en Y
    for persona in personas_atendidas:
        # Escribir cada persona en el PDF
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

    p.showPage()  # Finalizar la página
    p.save()  # Guardar el PDF
    buffer.seek(0)  # Reiniciar el buffer
    response.write(buffer.getvalue())  # Escribir contenido al response
    return response  # Devolver el PDF

# Vista para cargar un archivo CSV
def cargar_archivo(request):
    if request.method == 'POST':  # Si se envía el formulario
        form = UploadFileForm(request.POST, request.FILES)  # Crear instancia del formulario
        if form.is_valid():  # Validar el formulario
            archivo = request.FILES['file']  # Obtener el archivo subido

            if archivo.name.endswith('.csv'):  # Verificar si es un archivo CSV
                # Procesar CSV
                try:
                    lector = csv.DictReader(archivo.read().decode('utf-8').splitlines())  # Leer el archivo CSV
                    expected_fields = ['turno', 'nombre', 'apellido', 'edad']  # Campos esperados

                    if not all(field in lector.fieldnames for field in expected_fields):  # Verificar campos
                        raise ValueError("El archivo CSV no contiene todos los campos necesarios.")

                    for fila in lector:  # Iterar sobre las filas del CSV
                        print(f"Datos a crear: {fila}")  # Imprimir los datos leídos
                        Persona.objects.create(  # Crear nueva persona
                            turno=int(fila['turno']),
                            nombre=fila['nombre'],
                            apellido=fila['apellido'],
                            edad=int(fila['edad']),
                            atendido=fila['atendido'].lower() == 'true',  # Convertir a booleano
                        )
                    messages.success(request, 'CSV cargado con éxito.')  # Mensaje de éxito
                    
                    # Redirigir a la pantalla principal
                    return redirect('hola_mundo')  # Cambia 'hola_mundo' por el nombre de tu vista correspondiente

                except Exception as e:
                    messages.error(request, f'Error al procesar el CSV: {e}')  # Mensaje de error

    else:
        form = UploadFileForm()  # Crear formulario vacío

    return render(request, 'mi_app/cargar_archivo.html', {'form': form})  # Renderizar plantilla de carga

# Vista para ordenar personas por un atributo

def ordenar_lista_enlazada(request):
    atributo = request.GET.get('atributo', 'nombre')
    
    # Recuperar todas las personas desde la base de datos
    personas = Persona.objects.all()  # Recuperar todas las personas

    # Crear la lista enlazada y agregar las personas
    lista = ListaEnlazada()
    for persona in personas:
        lista.insertar(persona)

    # Ordenar la lista enlazada
    lista.ordenar(atributo)

    # Obtener la lista ordenada
    personas_ordenadas = lista.mostrar()
    
    # Asignar turnos en orden secuencial
    for index, persona in enumerate(personas_ordenadas, start=1):
        persona.turno = index
        persona.save()  # Guarda el nuevo turno en la base de datos

    return render(request, 'hola_mundo.html', {'personas': personas_ordenadas})

# Vista para buscar personas en la tabla por un atributo en especifico
def buscar_personas(request):
    valor = request.GET.get('q', '')
    atributo = request.GET.get('atributo', 'nombre')
    personas = Persona.objects.all()

    # Creamos la lista enlazada
    lista = ListaEnlazada()
    for persona in personas:
        lista.insertar(persona)
    
    # Buscamos todas las personas que coincidan
    personas_encontradas = lista.buscar_todas(valor, atributo)
    
    # Preparar el contexto para renderizar
    contexto = {
        'personas': personas,
        'personas_encontradas': personas_encontradas,  # Lista de personas que coinciden con la búsqueda
    }
    return render(request, 'hola_mundo.html', contexto)