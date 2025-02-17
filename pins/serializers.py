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
    # Include related Series data
    series = SeriesSerializer(read_only=True)
    # Format tags as a list
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Pin
        fields = '__all__'

    def get_tags(self, obj):
        return obj.get_tags_as_list()

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