from django.urls import reverse
from players.tests.test_models import CustomTestCase


class PlayersURLTests(CustomTestCase):

    def test_players_url(self):
        """
        Функция для тестирования доступа страниц по URL
        """
        post_slug = self.player.slug
        position_slug = self.position.slug
        club_slug = self.club.slug
        tag_slug = self.tag.slug

        pages = (
            "/",
            f"/post/{post_slug}/",
            f"/position/{position_slug}/",
            f"/club/{club_slug}/",
            "/about/",
            "/addpage/",
            "/contact/",
            f"/tag/{tag_slug}/",
            f"/edit/{post_slug}/",
            f"/delete/{post_slug}/",
        )

        for page in pages:
            self.client.login(username="test_name", password="test_pass")
            response = self.client.get(page)
            error = f"Ошибка: нет доступа до страницы {page}"
            self.assertEqual(response.status_code, 200, error)

    def test_players_uses_correct_template(self):
        """
        Функция для тестирования использования URL-адресом соответствующего шаблона.
        """
        template_url_names: dict = {
            reverse("home"): "players/index.html",
            reverse("post", args=[self.player.slug]): "players/post.html",
            reverse("position", args=[self.position.slug]): "players/index.html",
            reverse("club", args=[self.club.slug]): "players/index.html",
            reverse("about"): "players/about.html",
            reverse("add_page"): "players/addpage.html",
            reverse("contact"): "players/contact.html",
            reverse("tag", args=[self.tag.slug]): "players/index.html",
            reverse("edit_page", args=[self.player.slug]): "players/addpage.html",
            reverse("delete_page", args=[self.player.slug]): "players/deletepage.html",
        }

        for address, template in template_url_names.items():
            with self.subTest(address=address):
                self.client.login(username="test_name", password="test_pass")
                response = self.client.get(address)
                error = f"Ошибка: {address} ожидал шаблон {template}"
                self.assertTemplateUsed(response, template, error)
