from django.db import models

from django.core.validators import MinValueValidator

from api.productos.models import Producto


class Ruta(models.Model):
    NOMBRE = models.CharField(max_length=100)

    DIA = models.CharField(
        max_length=100,
        choices=(
            ("LUNES", "LUNES"),
            ("MARTES", "MARTES"),
            ("MIERCOLES", "MIERCOLES"),
            ("JUEVES", "JUEVES"),
            ("VIERNES", "VIERNES"),
            ("SABADO", "SABADO"),
            ("DOMINGO", "DOMINGO"),
        ),
    )

    REPARTIDOR = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.NOMBRE}, {self.DIA}"


class Cliente(models.Model):
    NOMBRE = models.CharField(max_length=100)

    # Esto solo facilida cargar la lista de clientes en la salida ruta
    RUTA = models.ForeignKey(
        Ruta, on_delete=models.SET_NULL, null=True, related_name="ruta_clientes"
    )

    def __str__(self):
        return str(self.NOMBRE)


class PrecioCliente(models.Model):
    CLIENTE = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="precios_cliente"
    )

    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.CLIENTE.NOMBRE}, {self.PRODUCTO.NOMBRE}, {self.PRECIO}"
