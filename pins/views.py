from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Series, Tag, Pin,UserCollection,Wishlist,TradingBoard
from .serializers import SeriesSerializer, TagSerializer, PinSerializer,UserCollectionSerializer,WishlistSerializer,TradingBoardSerializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import base64
from django.conf import settings
import os
from .image_search import generate_embedding
import logging
logger = logging.getLogger(__name__)  # Add this line
from django.core.files.base import ContentFile
import uuid
from datetime import datetime
from pinecone import Pinecone


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

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class CreatePinAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        image_base64 = request.data.get('image')
        if image_base64:
            try:
                # Split the data URI to get MIME type and base64 data
                if ';base64,' not in image_base64:
                    raise ValueError("Invalid data URI format")
                    
                mime_type, imgstr = image_base64.split(';base64,')
                # Extract the file extension from the MIME type (e.g., 'image/jpeg' -> 'jpeg')
                file_extension = mime_type.split('/')[-1] if '/' in mime_type else 'bin'
                
                # Add padding to the base64 string if necessary
                padding = '=' * (-len(imgstr) % 4)
                image_data = base64.b64decode(imgstr + padding)
                
                 # Create ContentFile with proper filename
                file_name = f"{uuid.uuid4().hex}.{file_extension}"
                image_file = ContentFile(image_data, name=file_name)
                
                test_embedding = generate_embedding(image_data)
                if test_embedding:
                    pc = Pinecone(api_key="pcsk_6pkmwU_5WC2wWq5j4KGq8S1QgLGnGkByZroAcSHRKLDh2YnjgfssPqomenV6ZkAPv7SaxM")
                    index_name = "pin-collection-image-prod"
                    index = pc.Index(index_name)
                    # Perform similarity search in Pinecone
                    search_results = index.query(vector=test_embedding, top_k=5, include_metadata=True)

                    # Display the results
                    for match in search_results["matches"]:
                        print(f"ID: {match['id']}, Score: {match['score']}")
                        print(f"Metadata: {match['metadata']}")
                        # Create Pin instance
                        pin_data = match['metadata']
                        release_date_str = pin_data.get('release_date', '').strip()
                        release_date = None 
                        if release_date_str.lower() == 'unknown' or not release_date_str:
                            release_date = None  # or use a default date like datetime(2000, 1, 1).date()
                        else:
                            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                        pin = Pin(
                        name=pin_data['name'],
                        series_name=pin_data['series'],
                        rarity=pin_data['rarity'],
                        origin=pin_data['origin'],
                        edition=pin_data['edition'],
                        release_date=release_date,
                        original_price=pin_data['original_price'],
                        sku=pin_data['sku'],
                        description=pin_data['description'],
                        image_url=pin_data['image_url'],
                        tags=pin_data.get('tags', '')  # Handle optional tags
                    )   
                        pin.image.save(file_name, image_file)
                        UserCollection.objects.create(pin=pin,user=request.user)
                        pin.save()
                        
                        print('saved')
                else:
                    return Response({'error':"Failed to generate embedding for the test image."},status=status.HTTP_400_BAD_REQUEST)
                
                
                
                return Response({'msg': 'Image uploaded successfully!'}, status=201)
            
            except Exception as e:
                # Log the error for debugging
                logger.error(f"Error processing image: {str(e)}", exc_info=True)
                return Response({'error': str(e)}, status=400)
        
        return Response({'error': 'No image provided'}, status=400)
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

class UserPinDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: PinSerializer()})
    def get(self, request, pin_id):
        """Get details of a specific pin in the user's collection."""
        try:
            pin_details = UserCollection.objects.get(user=request.user, id=pin_id)
            serializer = PinSerializer(pin_details.pin)  # Serialize the related Pin object
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserCollection.DoesNotExist:
            return Response({"error": "Pin not found in your collection."}, status=status.HTTP_404_NOT_FOUND)
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