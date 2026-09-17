from django import forms
from django.core.exceptions import ValidationError

from .models import Drink, Category, TagDrink


def validate_russian_name(value):
    allowed_chars = (
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
        'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
        '0123456789- '
    )

    if not set(value) <= set(allowed_chars):
        raise ValidationError(
            'Название должно содержать только русские символы, '
            'цифры, пробел и дефис.'
        )


class AddDrinkPlainForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label='Название',
        validators=[validate_russian_name]
    )

    slug = forms.SlugField(
        max_length=150,
        label='URL'
    )

    type = forms.CharField(
        max_length=100,
        label='Тип'
    )

    brand = forms.CharField(
        max_length=100,
        required=False,
        label='Бренд'
    )

    description = forms.CharField(
        required=False,
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'cols': 50,
            }
        )
    )

    available = forms.TypedChoiceField(
        choices=Drink.Availability.choices,
        coerce=lambda value: value == '1',
        label='Наличие'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Категория не выбрана',
        label='Категория'
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TagDrink.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Теги'
    )


class AddDrinkModelForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Категория не выбрана',
        label='Категория'
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TagDrink.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Теги'
    )

    class Meta:
        model = Drink

        fields = [
            'name',
            'slug',
            'type',
            'brand',
            'description',
            'photo',
            'available',
            'category',
            'tags',
        ]

        labels = {
            'name': 'Название',
            'slug': 'URL',
            'type': 'Тип',
            'brand': 'Бренд',
            'description': 'Описание',
            'available': 'Наличие',
            'photo': 'Изображение',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'cols': 50,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and len(name) > 50:
            raise ValidationError(
                'Длина названия не должна превышать 50 символов.'
            )

        return name


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Файл'
    )