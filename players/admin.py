from typing import Any

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from players.models import Club, Player, Position, Tag, Wife


class MarriedFilter(admin.SimpleListFilter):
    """
    Фильтр для выбора семейного положения игрока в админ-панели
    """

    title = "Статус футболистов"
    parameter_name = "status"

    def lookups(self, request, model_admin) -> list[tuple[str, str]]:
        return [
            ("married", "Женат"),
            ("free", "Не женат"),
        ]

    def queryset(self, request: Any, queryset: Any) -> Any:
        if self.value() == "married":
            return queryset.filter(club__isnull=False)
        elif self.value() == "free":
            return queryset.filter(club__isnull=True)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "content",
        "slug",
        "photo",
        "post_photo",
        "position",
        "club",
        "wife",
        "tags",
    ]
    readonly_fields = ["post_photo"]
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "post_photo",
        "time_create",
        "is_published",
        "position",
        "club",
        "brief_info",
    )
    list_display_links = ("title",)
    ordering = ("time_create", "title")
    list_editable = ("is_published",)
    list_per_page = 3
    actions = ["set_published", "set_draft"]
    search_fields = ["title__startswith", "position__name", "club__name"]
    list_filter = [MarriedFilter, "position__name", "club__name", "is_published"]
    save_on_top = True

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, player: Player) -> str:
        """
        Функция для подсчета количества сомволов в информации об игроке в админ-панели
        """
        return f"Описание {len(player.content)} символов"

    @admin.display(description="Изображение")
    def post_photo(self, player: Player) -> Any | str:
        """
        Функция для отображения изображения поста в админ-панели
        """
        if player.photo:
            return mark_safe(f"<img src='{player.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset) -> None:
        """
        Функция для опубликования поста в админ-панели
        """
        count = queryset.update(is_published=Player.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} записей")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset) -> None:
        """
        Функция для снятия поста с публикации в админ-панели
        """
        count = queryset.update(is_published=Player.Status.DRAFT)
        self.message_user(
            request, f"Снято {count} записей с публикации", messages.WARNING
        )


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")
    list_display_links = ("id", "name")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag")
    list_display_links = ("id", "tag")


@admin.register(Wife)
class WifeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age")
    list_display_links = ("id", "name")
