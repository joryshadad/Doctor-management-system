from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='existing', password='StrongPass123!')

    def test_authenticated_user_is_redirected_from_login_and_register(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse('login')), reverse('home'))
        self.assertRedirects(self.client.get(reverse('register')), reverse('home'))

    def test_login_creates_session(self):
        response = self.client.post(reverse('login'), {'username': 'existing', 'password': 'StrongPass123!'})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_registration_logs_user_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-user', 'password': 'StrongPass123!', 'password_confirm': 'StrongPass123!'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='new-user').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_login_stays_on_login_page(self):
        response = self.client.post(reverse('login'), {'username': 'existing', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
