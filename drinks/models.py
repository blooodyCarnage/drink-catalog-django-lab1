from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse(
            'category',
            kwargs={'cat_slug': self.slug}
        )

    def __str__(self):
        return self.name


class TagDrink(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название тега'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse(
            'tag',
            kwargs={'tag_slug': self.slug}
        )

    def __str__(self):
        return self.name


class DrinkMeta(models.Model):
    volume_ml = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Объём, мл'
    )
    package = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Упаковка'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна'
    )

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'

    def __str__(self):
        return f'{self.volume_ml or "—"} мл, {self.package or "без упаковки"}'


class AvailableDrinkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            available=Drink.Availability.AVAILABLE
        )


class Drink(models.Model):
    class Availability(models.IntegerChoices):
        NOT_AVAILABLE = 0, 'Нет в наличии'
        AVAILABLE = 1, 'В наличии'

    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        db_index=True,
        verbose_name='Slug'
    )

    type = models.CharField(
        max_length=100,
        verbose_name='Тип'
    )

    brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Бренд'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    available = models.BooleanField(
        choices=Availability.choices,
        default=Availability.AVAILABLE,
        verbose_name='Наличие'
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='drinks',
        verbose_name='Категория'
    )

    tags = models.ManyToManyField(
        TagDrink,
        blank=True,
        related_name='drinks',
        verbose_name='Теги'
    )

    meta = models.OneToOneField(
        DrinkMeta,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='drink',
        verbose_name='Дополнительная информация'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='drinks',
        verbose_name='Автор'
    )

    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='liked_drinks',
        verbose_name='Лайки'
    )

    disliked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='disliked_drinks',
        verbose_name='Дизлайки'
    )

    reposted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='reposted_drinks',
        verbose_name='Репосты'
    )

    objects = models.Manager()
    available_drinks = AvailableDrinkManager()

    class Meta:
        ordering = ['-time_create']

        indexes = [
            models.Index(
                fields=['-time_create']
            ),
        ]

        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'

        permissions = [
            (
                'can_publish_drink',
                'Может публиковать напитки',
            ),
        ]

    def get_absolute_url(self):
        return reverse(
            'drink_slug',
            kwargs={'drink_slug': self.slug}
        )

    def __str__(self):
        return self.name

class Comment(models.Model):
    drink = models.ForeignKey(
        Drink,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Напиток'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='drink_comments',
        verbose_name='Автор'
    )

    text = models.TextField(
        verbose_name='Текст комментария'
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text[:30]}'