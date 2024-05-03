from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from players.models import Club, Player, Position, Wife


class AddPostForm(forms.ModelForm):
    """
    Форма для добавления поста
    """

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        empty_label="Позиция не выбрана",
        label="Позиция",
    )
    club = forms.ModelChoiceField(
        queryset=Club.objects.all(), empty_label="Клуб не выбран", label="Клуб"
    )
    wife = forms.ModelChoiceField(
        queryset=Wife.objects.all(),
        required=False,
        empty_label="Не женат",
        label="Семейное положение",
    )

    class Meta:
        model = Player
        fields = [
            "title",
            "slug",
            "content",
            "photo",
            "is_published",
            "position",
            "club",
            "wife",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
        labels = {"slug": "URL"}

    def clean_title(self) -> Any:
        """
        Функция для валидации имени поста
        """
        title = self.cleaned_data["title"]

        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title
