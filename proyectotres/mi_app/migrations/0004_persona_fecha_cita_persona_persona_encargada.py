# Generated by Django 5.1.2 on 2024-10-19 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0003_persona_atendido'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='fecha_cita',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='persona_encargada',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]