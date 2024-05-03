from django.test import Client, TestCase
from django.urls import reverse
from users.forms import LoginUserForm
from users.models import User

username = "usertest2"
email = "user2@gmail.com"
password = "password_test_reg2"


class LoginViewTest(TestCase):
    def setUp(self):
        self.data = {"username": username, "email": email, "password": password}
        self.user_test = User.objects.create_user(**self.data)
        self.client.login(username=username, password=password)

    def test_correct_login_work(self):
        user_test = User.objects.filter(username="usertest2").first()
        response = self.client.post(
            reverse("users:login"),
            data={"username": user_test.username, "password": user_test.password},
        )
        self.assertTrue(response.context["user"].is_authenticated)
