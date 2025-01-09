from rest_framework import viewsets
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



# Render the main page (frontend)
def index(request):
    return render(request, 'index.html')

# Render a detail page for a specific pin
def pin_detail(request, pin_id):
    return render(request, 'pin_detail.html', {'pin_id': pin_id})