from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from players.forms import AddPostForm
from players.models import Club, Player, Tag
from players.utils import DataMixin


class PlayerHome(DataMixin, ListView):
    """
    Представление для отображения главной страницы
    """

    template_name = "players/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Player.published.all().select_related("position", "club")


class ShowPost(DataMixin, DetailView):
    """
    Представление для отображения детальной страницы поста
    """

    template_name = "players/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Player.published, slug=self.kwargs[self.slug_url_kwarg]
        )


class PlayerPosition(DataMixin, ListView):
    """
    Представление для отображения позиции
    """

    template_name = "players/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Player.published.filter(
            position__slug=self.kwargs["position_slug"]
        ).select_related("position")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = context["posts"][0].position
        return self.get_mixin_context(
            context, title="Позиция - " + position.name, position_selected=position.pk
        )


class PlayerClub(DataMixin, ListView):
    """
    Представление для отображения клуба
    """

    template_name = "players/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Player.published.filter(
            club__slug=self.kwargs["club_slug"]
        ).select_related("club")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = context["posts"][0].club
        return self.get_mixin_context(
            context, title="Клуб - " + club.name, club_selected=club.pk
        )


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    """
    Представление для добавления поста
    """

    form_class = AddPostForm
    template_name = "players/addpage.html"
    title_page = "Добавление статьи"
    permission_required = "players.add_player"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    """
    Представление для редактирования поста
    """

    model = Player
    fields = ["title", "content", "photo", "is_published", "position", "club", "tags"]
    template_name = "players/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"
    permission_required = "players.change_player"


class DeletePage(DataMixin, DeleteView):
    """
    Представление для удаления поста
    """

    model = Player
    template_name = "players/deletepage.html"
    context_object_name = "post"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"
    permission_required = "players.delete_player"


class TagPostList(DataMixin, ListView):
    """
    Представление для отображения списка тегов
    """

    template_name = "players/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Player.published.filter(
            tags__slug=self.kwargs["tag_slug"]
        ).select_related("position", "club")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context, title=f"Тег: {tag.tag}")


class Contact(DataMixin, TemplateView):
    """
    Представление для отображения страницы контактов
    """

    template_name = "players/contact.html"
    extra_context = {"title": "Наши контакты"}


class About(DataMixin, TemplateView):
    """
    Представление для отображения страницы информации о сайте
    """

    template_name = "players/about.html"
    extra_context = {"title": "О сайте"}


def page_not_found(request, exception):
    """
    Функция для отображения страницы ошибки
    """
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1><p>{exception}</p>")
