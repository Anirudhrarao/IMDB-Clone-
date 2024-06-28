from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "test@gmail.com",
            "password": "testcase@123",
            "password_confirmation": "testcase@123"
        }
        response = self.client.post(reverse('register'),data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testcase', password='testcase@123')
    
    def test_login(self):
        data = {
            "username": "testcase",
            "password": "testcase@123"
        }
        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
    
    def test_logout(self):
        data = {
            "username": "testcase",
            "password": "testcase@123"
        }

        response = self.client.post(reverse('token_obtain_pair'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + self.access_token)
        response = self.client.post(reverse('logout'), {'refresh': self.refresh_token}, format='json')


        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
