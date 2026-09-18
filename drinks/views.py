from django.shortcuts import render, redirect, get_object_or_404
from .models import Drink, Category, TagDrink
from .forms import (
    AddDrinkPlainForm,
    AddDrinkModelForm,
    UploadFileForm,
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .utils import DataMixin

import uuid
from pathlib import Path

from django.conf import settings

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

drinks_db = [
    {
        "id": 1,
        "name": "Кола",
        "slug": "cola",
        "type": "Газированный напиток",
        "brand": "Coca-Cola",
        "description": "Классический газированный безалкогольный напиток.",
        "is_available": True,
    },
    {
        "id": 2,
        "name": "Апельсиновый сок",
        "slug": "orange-juice",
        "type": "Сок",
        "brand": "Rich",
        "description": "Фруктовый напиток со вкусом апельсина.",
        "is_available": True,
    },
    {
        "id": 3,
        "name": "Минеральная вода",
        "slug": "mineral-water",
        "type": "Вода",
        "brand": "Borjomi",
        "description": "Минеральная вода для ежедневного употребления.",
        "is_available": True,
    },
    {
        "id": 4,
        "name": "Холодный чай",
        "slug": "cold-tea",
        "type": "Чай",
        "brand": "Lipton",
        "description": "Освежающий холодный чай.",
        "is_available": False,
    },
]


def index(request):
    data = {
        "title": "Каталог напитков",
        "description": (
            "Добро пожаловать в каталог напитков. "
            "Здесь представлены различные виды напитков."
        ),
    }
    return render(request, "drinks/index.html", data)


class AboutView(
    LoginRequiredMixin,
    DataMixin,
    TemplateView,
):
    template_name = 'drinks/about.html'

    extra_context = {
        'title': 'О сайте',
        'description': (
            'Drink Catalog — учебный проект на Django '
            'для работы с каталогом напитков.'
        ),
    }


class DrinkListView(DataMixin, ListView):
    template_name = 'drinks/drinks_list.html'
    context_object_name = 'drinks'

    def get_queryset(self):
        return (
            Drink.objects
            .select_related(
                'category',
                'meta'
            )
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        return self.get_mixin_context(
            context,
            title='Каталог напитков',
            selected_category=None,
            selected_tag=None,
        )

class DrinkCategory(DataMixin, ListView):
    template_name = 'drinks/drinks_list.html'
    context_object_name = 'drinks'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['cat_slug']
        )

        return (
            Drink.objects
            .filter(category=self.category)
            .select_related(
                'category',
                'meta'
            )
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        return self.get_mixin_context(
            context,
            title=f'Категория: {self.category.name}',
            selected_category=self.category,
            selected_tag=None,
        )

class DrinkTag(DataMixin, ListView):
    template_name = 'drinks/drinks_list.html'
    context_object_name = 'drinks'

    def get_queryset(self):
        self.tag = get_object_or_404(
            TagDrink,
            slug=self.kwargs['tag_slug']
        )

        return (
            self.tag.drinks
            .select_related(
                'category',
                'meta'
            )
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        return self.get_mixin_context(
            context,
            title=f'Тег: {self.tag.name}',
            selected_category=None,
            selected_tag=self.tag,
        )

def drink_by_id(request, drink_id):
    drink = get_object_or_404(
        Drink.objects.select_related('category', 'meta').prefetch_related('tags'),
        pk=drink_id
    )

    context = {
        'title': f'Напиток №{drink_id}',
        'drink_id': drink_id,
        'drink': drink,
    }

    return render(request, 'drinks/drink_id.html', context)


class ShowDrink(DataMixin, DetailView):
    model = Drink
    template_name = 'drinks/drink_slug.html'
    context_object_name = 'drink'

    slug_field = 'slug'
    slug_url_kwarg = 'drink_slug'

    def get_queryset(self):
        return (
            Drink.objects
            .select_related(
                'category',
                'meta'
            )
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        return self.get_mixin_context(
            context,
            title=f'Напиток: {self.object.name}',
            selected_category=self.object.category,
            selected_tag=None,
        )

class AddDrink(
    PermissionRequiredMixin,
    DataMixin,
    FormView,
):
    permission_required = 'drinks.add_drink'
    form_class = AddDrinkPlainForm
    template_name = 'drinks/add_plain.html'
    success_url = reverse_lazy('drinks')

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        tags = data.pop('tags')

        drink = Drink.objects.create(**data)
        drink.tags.set(tags)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title='Добавление напитка через FormView',
            selected_category=None,
            selected_tag=None,
        )

class CreateDrink(
    PermissionRequiredMixin,
    DataMixin,
    CreateView,
):
    permission_required = 'drinks.add_drink'

    form_class = AddDrinkModelForm
    template_name = 'drinks/add_model.html'
    success_url = reverse_lazy('drinks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title='Добавление напитка через CreateView',
            selected_category=None,
            selected_tag=None,
        )

def handle_uploaded_file(file):
    extension = Path(file.name).suffix
    unique_name = f'{uuid.uuid4()}{extension}'

    upload_dir = settings.MEDIA_ROOT / 'uploads'
    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_dir / unique_name

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return f'uploads/{unique_name}'

class UpdateDrink(
    PermissionRequiredMixin,
    DataMixin,
    UpdateView,
):
    permission_required = 'drinks.change_drink'

    model = Drink
    form_class = AddDrinkModelForm
    template_name = 'drinks/add_model.html'
    slug_url_kwarg = 'drink_slug'
    success_url = reverse_lazy('drinks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=f'Редактирование напитка: {self.object.name}',
            selected_category=self.object.category,
            selected_tag=None,
        )

class DeleteDrink(
    PermissionRequiredMixin,
    DataMixin,
    DeleteView,
):
    permission_required = 'drinks.delete_drink'

    model = Drink
    template_name = 'drinks/drink_confirm_delete.html'
    context_object_name = 'drink'
    slug_url_kwarg = 'drink_slug'
    success_url = reverse_lazy('drinks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=f'Удаление напитка: {self.object.name}',
            selected_category=self.object.category,
            selected_tag=None,
        )

class UploadFileView(
    LoginRequiredMixin,
    View,
):
    template_name = 'drinks/upload_file.html'

    def get(self, request):
        context = {
            'title': 'Загрузка файла',
            'form': UploadFileForm(),
            'uploaded_file': None,
        }

        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request):
        form = UploadFileForm(
            request.POST,
            request.FILES
        )

        uploaded_file = None

        if form.is_valid():
            uploaded_file = handle_uploaded_file(
                form.cleaned_data['file']
            )

            form = UploadFileForm()

        context = {
            'title': 'Загрузка файла',
            'form': form,
            'uploaded_file': uploaded_file,
        }

        return render(
            request,
            self.template_name,
            context
        )

def search(request):
    drink_type = request.GET.get("type", "")
    brand = request.GET.get("brand", "")

    data = {
        "title": "Поиск напитков",
        "drink_type": drink_type,
        "brand": brand,
        "get_params": request.GET.dict(),
    }

    return render(request, "drinks/search.html", data)


def archive(request, year):
    if year > 2026:
        return redirect("home")

    data = {
        "title": "Архив каталога",
        "year": year,
    }

    return render(request, "drinks/archive.html", data)


def go_home(request):
    return redirect("home")


def page_not_found(request, exception):
    data = {
        "title": "Ошибка 404",
    }

    return render(
        request,
        "drinks/404.html",
        data,
        status=404
    )