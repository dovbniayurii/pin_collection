from rest_framework.routers import DefaultRouter
from .views import SeriesViewSet, TagViewSet, PinViewSet,CreatePinAPIView,UserPinDetailAPIView,UserCollectionAPIView,WishlistAPIView,TradingBoardAPIView
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
    path('user-collection/', UserCollectionAPIView.as_view(), name='user-collection'),
    path('pin-details/<int:pin_id>/', UserPinDetailAPIView.as_view(), name='user-collection'),
    path('wishlist/', WishlistAPIView.as_view(), name='wishlist'),
    path('trading-board/', TradingBoardAPIView.as_view(), name='trading_board'),
    path('create-pin/', CreatePinAPIView.as_view(), name='create-pin'),
    #path('api/', include(router.urls)),  # Include the API routes under `/api/`

]
