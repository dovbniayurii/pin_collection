from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Series, Tag, Pin
from .serializers import SeriesSerializer, TagSerializer, PinSerializer
from django.shortcuts import render


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PinViewSet(viewsets.ModelViewSet):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        pin = self.get_object()
        serializer = self.get_serializer(pin)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pin = self.get_object()
        serializer = self.get_serializer(pin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pin = self.get_object()
        pin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



# Render the main page (frontend)
def index(request):
    return render(request, 'index.html')

# Render a detail page for a specific pin
def pin_detail(request, pin_id):
    return render(request, 'pin_detail.html', {'pin_id': pin_id})    