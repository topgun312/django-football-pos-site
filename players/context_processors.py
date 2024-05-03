from typing import Any

from players.utils import menu


def get_players_context(request: Any) -> Any:
    """
    Фунцкия для создания шаблонного контекстного процессора для отображения меню сайта
    """
    return {"mainmenu": menu}
