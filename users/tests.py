from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import PinUser

class UserTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.user_data = {
            'useremail': 'testuser@example.com',
            'password': 'password123'
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PinUser.objects.count(), 1)
        self.assertEqual(PinUser.objects.get().useremail, self.user_data['useremail'])

    def test_user_signin(self):
        self.client.post(self.signup_url, self.user_data)  # Create user first
        response = self.client.post(self.signin_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Assuming access token is returned on successful signin

    def test_signup_with_existing_email(self):
        self.client.post(self.signup_url, self.user_data)  # Create user first
        response = self.client.post(self.signup_url, self.user_data)  # Try to create again
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_invalid_credentials(self):
        response = self.client.post(self.signin_url, {
            'useremail': 'wronguser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)