from django.test import TestCase
from .models import Pin, Series

class PinModelTest(TestCase):
    def setUp(self):
        self.series = Series.objects.create(name="Test Series", description="A test series.")
        self.pin = Pin.objects.create(
            name="Test Pin",
            series=self.series,
            rarity="Common",
            origin="Test Origin",
            edition="Test Edition",
            release_date="2023-01-01",
            original_price=10.00,
            sku="TEST123",
            description="A test pin description.",
            image_url="http://example.com/image.jpg",
            image="pin_images/test_pin.jpg",
            tags="tag1, tag2"
        )

    def test_pin_creation(self):
        self.assertEqual(self.pin.name, "Test Pin")
        self.assertEqual(self.pin.series.name, "Test Series")
        self.assertEqual(self.pin.rarity, "Common")
        self.assertEqual(self.pin.origin, "Test Origin")
        self.assertEqual(self.pin.edition, "Test Edition")
        self.assertEqual(self.pin.release_date.strftime("%Y-%m-%d"), "2023-01-01")
        self.assertEqual(self.pin.original_price, 10.00)
        self.assertEqual(self.pin.sku, "TEST123")
        self.assertEqual(self.pin.description, "A test pin description.")
        self.assertEqual(self.pin.image_url, "http://example.com/image.jpg")
        self.assertEqual(self.pin.image, "pin_images/test_pin.jpg")
        self.assertEqual(self.pin.tags, "tag1, tag2")

    def test_pin_str(self):
        self.assertEqual(str(self.pin), "Test Pin")