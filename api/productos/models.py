from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Producto(models.Model):

    NOMBRE = models.CharField(max_length=100)

    CANTIDAD = models.IntegerField(validators=[MinValueValidator(0)])

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    # RECUERDA NO PONER NADA QUE SE PUEDE VOLVER NULL AQUI
    def __str__(self):
        return f"{self.NOMBRE}, {self.CANTIDAD}, {self.PRECIO}"