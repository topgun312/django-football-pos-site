from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from users.forms import RegisterUserForm
from users.models import User

register_data = {
    "username": "usertest",
    "email": "email@gmail.com",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "password1": "password_test_reg",
    "password2": "password_test_reg",
}


class RegistrationTest(TestCase):

    def test_exists_page(self):
        response = self.client.get(reverse("users:register"))
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_user(self):
        response = self.client.post(reverse("users:register"), data=register_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 1)
