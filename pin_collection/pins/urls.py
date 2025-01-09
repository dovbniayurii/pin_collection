from rest_framework.routers import DefaultRouter
from .views import SeriesViewSet, TagViewSet, PinViewSet
from django.urls import path, include
from . import views

# Initialize the router for API routes
router = DefaultRouter()
router.register('series', SeriesViewSet)
router.register('tags', TagViewSet)
router.register('pins', PinViewSet)

# Combine API and frontend routes
urlpatterns = [
    path('', views.index, name='index'),  # Frontend index page
    path('pins/<int:pin_id>/', views.pin_detail, name='pin-detail'),  # Detail page
    path('api/', include(router.urls)),  # Include the API routes under `/api/`

]
