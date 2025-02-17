from django.db import models
from users.models import PinUser

class Series(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Pin(models.Model):
    name = models.CharField(max_length=255)
    series_name = models.CharField(max_length=255, default='Unknown')
    rarity = models.CharField(max_length=50)
    origin = models.CharField(max_length=255)
    edition = models.CharField(max_length=100, blank=True)
    release_date = models.DateField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    image = models.ImageField(upload_to="pin_images/")
    tags = models.TextField(blank=True)  # Comma-separated string of tags

    def __str__(self):
        return self.name

    def get_tags_as_list(self):
        """Utility method to get tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    

class UserCollection(models.Model):
    user = models.ForeignKey(PinUser, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.useremail} - {self.pin.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(PinUser, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.useremail} - Wishlist - {self.pin.name}"


#class Tradelist(models.Model):
#    user = models.ForeignKey(PinUser, on_delete=models.CASCADE)
#    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
#    added_at = models.DateTimeField(auto_now_add=True)

 #   def __str__(self):
 #       return f"{self.user.useremail} - Wishlist - {self.pin.name}"
class TradingBoard(models.Model):
    user = models.ForeignKey(PinUser, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.useremail} - Trading - {self.pin.name}"
