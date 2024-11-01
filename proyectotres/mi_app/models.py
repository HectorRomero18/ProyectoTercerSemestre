from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    turno = models.PositiveIntegerField(default=0)
    atendido = models.BooleanField(default=False)
    fecha_cita = models.DateField(null=True, blank=True)  # Campo para fecha de cita
    persona_encargada = models.CharField(max_length=100, null=True, blank=True)  # Campo para persona encargada
    

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
