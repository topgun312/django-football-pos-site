from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    """
    Функция для перевода русских букв в английские
    """
    d = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "c",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ы": "y",
        "ъ": "",
        "э": "r",
        "ю": "yu",
        "я": "ya",
    }

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    """
    Менеджер для выборки только опубликованных постов
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Player.Status.PUBLISHED)


class Player(models.Model):
    """
    Модель футболиста
    """

    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="Слаг"
    )
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/",
        default=None,
        blank=True,
        null=True,
        verbose_name="Фото",
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус",
    )
    position = models.ForeignKey(
        "Position",
        on_delete=models.PROTECT,
        related_name="positions",
        verbose_name="Позиция",
    )
    club = models.ForeignKey(
        "Club", on_delete=models.PROTECT, related_name="clubs", verbose_name="Клуб"
    )
    tags = models.ManyToManyField(
        "Tag", blank=True, related_name="tags", verbose_name="Тег"
    )
    wife = models.OneToOneField(
        "Wife",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wife",
        verbose_name="Жена",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        default=None,
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известный футболист"
        verbose_name_plural = "Известные футболисты"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(translit_to_eng(self.title))
        super().save(*args, **kwargs)


class Position(models.Model):
    """
    Модель позиции на поле
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name="Слаг"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("position", kwargs={"position_slug": self.slug})


class Club(models.Model):
    """
    Модель клуба
    """

    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    country = models.CharField(max_length=100, null=False, verbose_name="Страна")
    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name="Слаг"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("club", kwargs={"club_slug": self.slug})


class Tag(models.Model):
    """
    Модель тега
    """

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})


class Wife(models.Model):
    """
    Модель жены
    """

    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField(null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Жена"
        verbose_name_plural = "Жены"

    def __str__(self):
        return self.name
