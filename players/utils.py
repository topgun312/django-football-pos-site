menu = [
    {"title": "Главная", "url_name": "home"},
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Админ-панель", "url_name": "admin:index"},
]


class DataMixin:
    """
    Класс-миксин для реализации пагинатора сайта
    """

    title_page = None
    position_selected = None
    extra_context = {}
    paginate_by = 3

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

        if self.position_selected is not None:
            self.extra_context["position_selected"] = self.position_selected

    def get_mixin_context(self, context, **kwargs):
        context["position_selected"] = None
        context.update(kwargs)
        return context
