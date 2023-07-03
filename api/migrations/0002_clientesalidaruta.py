# Generated by Django 4.1.7 on 2023-02-28 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteSalidaRuta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('STATUS', models.CharField(choices=[('PENDIENTE', 'PENDIENTE'), ('VISITADO', 'VISITADO')], max_length=100)),
                ('CLIENTE_RUTA', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.cliente')),
                ('SALIDA_RUTA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salida_ruta_clientes', to='api.salidaruta')),
            ],
        ),
    ]
