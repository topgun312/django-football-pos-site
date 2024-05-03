from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from players.forms import AddPostForm
from players.models import Club, Position, Tag, Wife
from players.tests.test_models import CustomTestCase

User = get_user_model()
name = "test_name_2"
slug = "test_slug_2"
age = 31
country = "England"
tag = "test_tag_2"


class AddPostFormTest(CustomTestCase):

    def setUp(self):
        self.client = Client()
        self.position_2 = Position.objects.create(name=name, slug=slug)
        self.club_2 = Club.objects.create(name=name, country=country, slug=slug)
        self.tag_2 = Tag.objects.create(tag=tag, slug=slug)
        self.wife_2 = Wife.objects.create(name=name, age=age)

        self.form_data = {
            "title": "test_title_2",
            "slug": "test_slug_2",
            "content": "test_content_2",
            "photo": settings.DEFAULT_USER_IMAGE,
            "is_published": True,
            "position": 2,
            "club": 2,
            "wife": 2,
            "tags": [1, 2],
        }

    def test_form(self):
        """
        Функция для тестирования валидности входных данных формы добавления поста
        """
        form = AddPostForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_forms_correct_work(self):
        """
        Функция для тестирования корректной работы формы при добавлении записей
        """
        self.client.login(username="test_name", password="test_pass")
        response = self.client.post(
            reverse("add_page"), data=self.form_data, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
