from typing import Any

from django import template
from django.db.models import Count
from players.models import Club, Position, Tag

register = template.Library()


@register.inclusion_tag("players/list_positions.html")
def show_positions(position_selected: int = 0) -> dict[str, int]:
    """
    Функция для добавления включающего тега по позициям
    """
    positions = Position.objects.annotate(total=Count("positions")).filter(total__gt=0)
    return {"positions": positions, "position_selected": position_selected}


@register.inclusion_tag("players/list_clubs.html")
def show_clubs(club_selected: int = 0) -> dict[str, int]:
    """
    Функция для добавления включающего тега по клубам
    """
    clubs = Club.objects.annotate(total=Count("clubs")).filter(total__gt=0)
    return {"clubs": clubs, "club_selected": club_selected}


@register.inclusion_tag("players/list_tags.html")
def show_tags() -> dict[str, Any]:
    """
    Функция для добавления включающего тега по тегам
    """
    tags = Tag.objects.annotate(total=Count("tags")).filter(total__gt=0)
    return {"tags": tags}
