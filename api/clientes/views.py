from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Cliente, Ruta
from .serializers import ClienteSerializer, RutaSerializer

@api_view(['GET'])
def cliente_list(request):

    queryset = Cliente.objects.all()
    serializer = ClienteSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def crear_cliente(request):

    serializer = ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def cliente_detail(request, pk):

    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ClienteSerializer(cliente)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def modificar_cliente(request, pk):

    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET'])
def ruta_list(request):

    queryset = Ruta.objects.all()

    serializer = RutaSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def crear_ruta(request):

    serializer = RutaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def ruta_detail(request, pk):
    
    try:
        ruta = Ruta.objects.get(pk=pk)
    except Ruta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = RutaSerializer(ruta)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def modificar_ruta(request, pk):
    try:
        ruta = Ruta.objects.get(pk=pk)
    except Ruta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = RutaSerializer(ruta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        ruta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)