from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from players.models import Club, Player, Position, Tag, Wife

name = "test_name"
title = "test_title"
password = "test_pass"
slug = "test_slug"
country = "test_country"
tag = "test_tag"
age = 25
photo = settings.DEFAULT_USER_IMAGE
content = "Самый лучший футболист"


players = {
    "name": name,
    "title": title,
    "tag": tag,
    "slug": slug,
    "photo": photo,
    "content": content,
    "is_published": 1,
    "country": country,
}


class CustomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_superuser(
            username=name, email="qwerty@gmail.com", password=password
        )
        cls.position = Position.objects.create(name=name, slug=slug)
        cls.club = Club.objects.create(name=name, country=country, slug=slug)
        cls.tag = Tag.objects.create(tag=tag, slug=slug)
        cls.wife = Wife.objects.create(name=name, age=age)
        cls.player = Player.objects.create(
            title=title,
            slug=slug,
            photo=photo,
            content=content,
            is_published=1,
            position=cls.position,
            club=cls.club,
            wife=cls.wife,
            author=cls.author,
        )
        tags = Tag.objects.all()
        cls.player.tags.add(*tags.values_list("id", flat=True))


class PlayerModelsTest(CustomTestCase):
    def test_player_model(self):
        """
        Функция для тестирования добавления обьектов в модели приложения
        """
        position_model = Position.objects.get(slug=self.position.slug)
        club_model = Club.objects.get(slug=self.club.slug)
        tag_model = Tag.objects.get(slug=self.tag.slug)
        wife_model = Wife.objects.get(name=self.wife.name)
        player_model = Player.objects.get(slug=self.player.slug)
        self.assertEqual(position_model.name, players["name"])
        self.assertEqual(club_model.country, players["country"])
        self.assertEqual(tag_model.tag, players["tag"])
        self.assertEqual(wife_model.name, players["name"])
        self.assertEqual(player_model.title, players["title"])
