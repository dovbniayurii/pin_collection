from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('user-signup')
        self.signin_url = reverse('user-signin')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])

    def test_user_signin(self):
        self.client.post(self.signup_url, self.user_data)  # Create user first
        response = self.client.post(self.signin_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Assuming token is returned on successful signin

    def test_signup_with_existing_email(self):
        self.client.post(self.signup_url, self.user_data)  # Create user first
        response = self.client.post(self.signup_url, self.user_data)  # Try to create again
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signin_with_invalid_credentials(self):
        response = self.client.post(self.signin_url, {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)