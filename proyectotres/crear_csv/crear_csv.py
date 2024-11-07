import os
import csv

# Datos de ejemplo
personas = [
    ["nombre", "apellido", "edad", "turno", "atendido", "fecha_cita", "persona_encargada"],
    ["Lionel", "Messi", 30, 1, 1, "", "María"],
    ["Jude", "Bellingham", 25, 2, 0, "", "Carlos"],
    ["Florian", "Wirtz", 25, 3, 0, "", "Fred"],
    ["Dani", "Olmo", 25, 4, 0, "", "Karla"],
    ["Lamine", "Yamal", 25, 5, 0, "", "Victor"],
]

# Definir la ruta (en el mismo directorio del script)
nombre_archivo = 'personas.csv'

# Crear y escribir en el archivo CSV en el mismo directorio
with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerows(personas)

print("Archivo CSV creado con éxito.")
