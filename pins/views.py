from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Series, Tag, Pin,UserCollection,Wishlist,TradingBoard
from .serializers import SeriesSerializer, TagSerializer, PinSerializer,UserCollectionSerializer,WishlistSerializer,TradingBoardSerializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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


class UserCollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserCollectionSerializer(many=True)},  # Use 'responses' for GET
    )
    # Retrieve the user's collection
    def get(self, request):
        user_collection = UserCollection.objects.filter(user=request.user)
        serializer = UserCollectionSerializer(user_collection, many=True)
        return Response(serializer.data)
    def get(self, request,pin_id):
        try:
            pin_details = UserCollection.objects.get(user=request.user, pin__id=pin_id)
            serializer = PinSerializer(pin_details.pin)  # Serialize the related pin object
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserCollection.DoesNotExist:
            return Response({"error": "Pin not found in your collection."}, status=status.HTTP_404_NOT_FOUND)
    # Add a pin to the user's collection (POST method)
    #@swagger_auto_schema(
     #   request_body=UserCollectionSerializer,  # Only for methods that send data
     #   responses={201: UserCollectionSerializer()}
    #)
    #def post(self, request):
     #   request.data['user'] = request.user.id
      #  serializer = UserCollectionSerializer(data=request.data)
       # if serializer.is_valid():
        #    serializer.save()
         #   return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for user wishlists
class WishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Retrieve the user's wishlist
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)
    
# API view for user wishlists
class TradingBoardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Retrieve the user's wishlist
    def get(self, request):
        trading = TradingBoard.objects.filter(user=request.user)
        serializer = TradingBoardSerializer(trading, many=True)
        return Response(serializer.data)