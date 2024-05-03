from django.conf import settings
from django.test import Client
from django.urls import reverse
from players.forms import AddPostForm
from players.models import Club, Player, Position, Tag, Wife
from players.tests.test_models import CustomTestCase


class PlayersViewsTests(CustomTestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username="test_name", password="test_pass")
        self.tag_3 = Tag.objects.create(tag="test_tag_3", slug="test_slug_3")
        self.wife_3 = Wife.objects.create(name="test_name_3", age=33)
        self.position_3 = Position.objects.create(
            name="test_name_3", slug="test_slug_3"
        )
        self.club_3 = Club.objects.create(
            name="test_name_3", country="test_country_3", slug="test_slug_3"
        )
        tags = Tag.objects.all()
        self.player.tags.add(*tags.values_list("id", flat=True))

    def test_playerhome_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в index.html
        """
        response = self.client.get(reverse("home"))
        home_view_text = {
            response.context["posts"][0].title: self.player.title,
            response.context["posts"][0].photo: self.player.photo,
            response.context["posts"][0].content: self.player.content,
        }
        for key, value in home_view_text.items():
            self.assertEqual(home_view_text[key], value)

    def test_showpost_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в post.html
        """
        response = self.client.get(reverse("post", args=[self.player.slug]))
        showpost_view_text = {
            response.context["post"].title: self.player.title,
            response.context["post"].photo: self.player.photo,
            response.context["post"].content: self.player.content,
        }
        for key, value in showpost_view_text.items():
            self.assertEqual(showpost_view_text[key], value)

    def test_playerposition_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в index.html
        """
        response = self.client.get(reverse("position", args=[self.position.slug]))
        playerposition_view_text = {
            response.context["posts"][0].position.name: self.position.name,
        }
        for key, value in playerposition_view_text.items():
            self.assertEqual(playerposition_view_text[key], value)

    def test_playerclub_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в index.html
        """
        response = self.client.get(reverse("club", args=[self.club.slug]))
        playerclub_view_text = {
            response.context["posts"][0].club.name: self.club.name,
        }
        for key, value in playerclub_view_text.items():
            self.assertEqual(playerclub_view_text[key], value)

    def test_addpost_page(self):
        """
        Функция для тестирования добавления записи
        """
        self.data = {
            "title": "test_title_3",
            "slug": "test_slug_3",
            "photo": settings.DEFAULT_USER_IMAGE,
            "content": "test_content_3",
            "is_published": True,
            "position": self.position_3,
            "club": self.club_3,
            "wife": self.wife_3,
            "tags": [self.tag, self.tag_3],
            "author": self.author,
        }

        form = AddPostForm(data=self.data)
        form.save()
        self.assertTrue(Player.published.filter(title="test_title_3").exists())

    def test_update_page(self):
        """
        Функция для тестирования изменения данных записи
        """
        self.player_update = Player.published.filter(title="test_title").first()
        response = self.client.post(
            reverse("edit_page", args=[self.player_update.slug]),
            data={"title": "test_title_4", "content": "test_content_4"},
        )
        self.player_update.refresh_from_db()
        self.assertTrue(response.status_code == 200)

    def test_delete_page(self):
        """
        Функция для тестирования удаления записи
        """
        players_count = Player.objects.all().count()
        self.player_delete = Player.published.filter(title="test_title").first()
        self.client.post(reverse("delete_page", args=[self.player_delete.slug]))
        self.assertEqual(Player.objects.all().count(), players_count - 1)

    def test_contact_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в contact.html
        """
        response = self.client.get(reverse("contact"))
        contact_view_text = {response.context["title"][0].title: "Наши контакты"}
        for key, value in contact_view_text.items():
            self.assertEqual(contact_view_text[key], value)

    def test_about_page(self):
        """
        Функция для тестирования правильного формирования контекста шаблона в about.html
        """
        response = self.client.get(reverse("about"))
        about_view_text = {response.context["title"][0].title: "О сайте"}
        for key, value in about_view_text.items():
            self.assertEqual(about_view_text[key], value)
