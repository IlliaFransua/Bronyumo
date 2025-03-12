from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from apps.accounts.serializers import SignUpSerializer

# Create your tests here.


class SignUpAPITest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "teST#1pass",
        }
        self.url = '/accounts/api/sign-up/'

    def test_successful_signup(self):
        response = self.client.post(self.url, data=self.user_data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_duplicate_username(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="teST#1pass")
        response = self.client.post(self.url, data=self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'][0], 'Имя пользователя уже занято.')

    def test_duplicate_email(self):
        User.objects.create_user(username="testuser2", email="testuser@example.com", password="teST#1pass12")
        response = self.client.post(self.url, data=self.user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'Этот email уже используется.')


class PasswordCreateAPITest(TestCase):

    def setUp(self):
        self.valid_password = "Valid123!"
        self.too_short_password = "Short1"
        self.too_long_password = "A" * 65
        self.no_digit_password = "NoDigitPassword!"
        self.no_lowercase_password = "NOLOWERCASE123!"
        self.no_uppercase_password = "nouppercase123!"
        self.no_special_char_password = "NoSpecial123"

    def test_valid_password(self):
        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.valid_password})

        self.assertTrue(serializer.is_valid())

    def test_too_short_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.too_short_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Пароль должен содержать не менее 8 символов.")

    def test_too_long_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.too_long_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Пароль пароль слишком длинный")

    def test_no_digit_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.no_digit_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Пароль должен содержать хотя бы одну цифру.")

    def test_no_lowercase_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.no_lowercase_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0],
                         "Пароль должен содержать хотя бы одну строчную букву.")

    def test_no_uppercase_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.no_uppercase_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0],
                         "Пароль должен содержать хотя бы одну прописную букву.")

    def test_no_special_char_password(self):

        serializer = SignUpSerializer(data={"username": "testuser",
                                            "email": "testuser@example.com",
                                            "password": self.no_special_char_password})
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0],
                         "Пароль должен содержать хотя бы один специальный символ.")
