# Generated by Django 4.1.7 on 2023-02-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_clientesalidaruta'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucionsalidaruta',
            name='ADMINISTRADOR',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devolucionsalidaruta',
            name='ATIENDE',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='devolucionsalidaruta',
            name='REPARTIDOR',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='clientesalidaruta',
            name='STATUS',
            field=models.CharField(choices=[('PENDIENTE', 'PENDIENTE'), ('VISITADO', 'VISITADO'), ('CANCELADO', 'CANCELADO')], max_length=100),
        ),
    ]
