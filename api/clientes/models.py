from django.db import models

from django.core.validators import MinValueValidator

from api.productos.models import Producto


class Ruta(models.Model):
    NOMBRE = models.CharField(max_length=100)

    # Si vamos a crear una ruta por cada dia. Al momento de registrar un usuario con una casilla le damos a escoger al usuario que dias de la ruta se deben considerar. Como ya existen los siete dias para esa ruta (o las siete rutas en realidad) solo es cosa de anadir el ciente a todas esas rutas

    # un cliente puede tener muchas rutas

    # Al momento de crear una ruta en realidad se cran siete, una por cada dia
    #
    # Debe ser posible eliminar todos los clientes en una ruta (los siete dias) o en cualquiera de los siete dias de esa ruta.

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
