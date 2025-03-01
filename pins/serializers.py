from rest_framework import serializers
from .models import Series, Tag, Pin,UserCollection,Wishlist,TradingBoard

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = [
            'name', 'series_name', 'rarity', 'origin', 'edition', 'release_date',
            'original_price', 'sku', 'description', 'image_url', 'image', 'tags'
        ]


class UserCollectionSerializer(serializers.ModelSerializer):
    # Include related Pin data
    pin = PinSerializer(read_only=True)

    class Meta:
        model = UserCollection
        fields = '__all__'

# Serializer for the Wishlist model
class WishlistSerializer(serializers.ModelSerializer):
    # Include related Pin data
    pin = PinSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
        
class TradingBoardSerializer(serializers.ModelSerializer):
    # Include related Pin data
    pin = PinSerializer(read_only=True)

    class Meta:
        model = TradingBoard
        fields = '__all__'