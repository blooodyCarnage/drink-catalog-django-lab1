from django.shortcuts import render, redirect, get_object_or_404
from .models import Drink, Category, TagDrink
from .forms import (
    AddDrinkPlainForm,
    AddDrinkModelForm,
    UploadFileForm,
)
import uuid
from pathlib import Path

from django.conf import settings

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


def about(request):
    data = {
        "title": "О сайте",
        "description": (
            "Drink Catalog — учебный проект на Django "
            "для работы с каталогом напитков."
        ),
    }
    return render(request, "drinks/about.html", data)


def drinks_list(request):
    drinks = (
        Drink.objects
        .select_related('category', 'meta')
        .prefetch_related('tags')
        .all()
    )

    drink_names = [drink.name for drink in drinks]

    context = {
        'title': 'Каталог напитков',
        'drinks': drinks,
        'drink_names': drink_names,
        'categories': Category.objects.all(),
        'tags': TagDrink.objects.all(),
        'selected_category': None,
        'selected_tag': None,
    }

    return render(request, 'drinks/drinks_list.html', context)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)

    drinks = (
        Drink.objects
        .select_related('category', 'meta')
        .prefetch_related('tags')
        .filter(category=category)
    )

    context = {
        'title': f'Категория: {category.name}',
        'drinks': drinks,
        'drink_names': [drink.name for drink in drinks],
        'categories': Category.objects.all(),
        'tags': TagDrink.objects.all(),
        'selected_category': category,
        'selected_tag': None,
    }

    return render(request, 'drinks/drinks_list.html', context)

def show_tag(request, tag_slug):
    tag = get_object_or_404(TagDrink, slug=tag_slug)

    drinks = (
        tag.drinks
        .select_related('category', 'meta')
        .prefetch_related('tags')
        .all()
    )

    context = {
        'title': f'Тег: {tag.name}',
        'drinks': drinks,
        'drink_names': [drink.name for drink in drinks],
        'categories': Category.objects.all(),
        'tags': TagDrink.objects.all(),
        'selected_category': None,
        'selected_tag': tag,
    }

    return render(request, 'drinks/drinks_list.html', context)

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


def drink_by_slug(request, drink_slug):
    drink = get_object_or_404(
        Drink.objects.select_related('category', 'meta').prefetch_related('tags'),
        slug=drink_slug
    )

    context = {
        'title': f'Напиток: {drink.name}',
        'drink_slug': drink_slug,
        'drink': drink,
    }

    return render(request, 'drinks/drink_slug.html', context)

def add_plain(request):
    if request.method == 'POST':
        form = AddDrinkPlainForm(request.POST)

        if form.is_valid():
            drink = Drink.objects.create(
                name=form.cleaned_data['name'],
                slug=form.cleaned_data['slug'],
                type=form.cleaned_data['type'],
                brand=form.cleaned_data['brand'],
                description=form.cleaned_data['description'],
                available=form.cleaned_data['available'],
                category=form.cleaned_data['category'],
            )

            drink.tags.set(form.cleaned_data['tags'])

            return redirect('drinks')
    else:
        form = AddDrinkPlainForm()

    context = {
        'title': 'Добавление напитка',
        'form': form,
    }

    return render(
        request,
        'drinks/add_plain.html',
        context
    )

def add_model(request):
    if request.method == 'POST':
        form = AddDrinkModelForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('drinks')
    else:
        form = AddDrinkModelForm()

    context = {
        'title': 'Добавление напитка через ModelForm',
        'form': form,
    }

    return render(
        request,
        'drinks/add_model.html',
        context
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

def upload_file(request):
    uploaded_file = None

    if request.method == 'POST':
        form = UploadFileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            uploaded_file = handle_uploaded_file(
                form.cleaned_data['file']
            )

            form = UploadFileForm()
    else:
        form = UploadFileForm()

    context = {
        'title': 'Загрузка файла',
        'form': form,
        'uploaded_file': uploaded_file,
    }

    return render(
        request,
        'drinks/upload_file.html',
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