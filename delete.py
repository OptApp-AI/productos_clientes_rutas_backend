from rest_framework import serializers
from .models import Padre, Hijo



class HijoSerializer(serializers.ModelSerializer):
    padre = serializers.SerializerMethodField()

    class Meta:
        model = Hijo
        fields = ('id', 'nombre', 'padre')

    def get_padre(self, obj):
        return obj.padre.nombre


class PadreSerializer(serializers.ModelSerializer):

    hijos = HijoSerializer(many=True, read_only=True)
    class Meta:
        model = Padre
        fields = ('id', 'nombre')