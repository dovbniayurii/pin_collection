from django.contrib import admin
from .models import Series, Tag, Pin,Wishlist,UserCollection,TradingBoard

admin.site.register(Series)
admin.site.register(Tag)
admin.site.register(Pin)
admin.site.register(Wishlist)
admin.site.register(UserCollection)
admin.site.register(TradingBoard)

