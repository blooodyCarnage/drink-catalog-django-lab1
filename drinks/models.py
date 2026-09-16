from django.db import models
from django.urls import reverse


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

    objects = models.Manager()
    available_drinks = AvailableDrinkManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'

    def get_absolute_url(self):
        return reverse('drink_slug', kwargs={'drink_slug': self.slug})

    def __str__(self):
        return self.name