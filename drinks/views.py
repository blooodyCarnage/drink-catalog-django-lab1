from django.shortcuts import redirect, render


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
    drink_names = [drink["name"] for drink in drinks_db]

    data = {
        "title": "Каталог напитков",
        "drinks": drinks_db,
        "drink_names": drink_names,
    }

    return render(request, "drinks/drinks_list.html", data)


def drink_by_id(request, drink_id):
    drink = next(
        (
            drink
            for drink in drinks_db
            if drink["id"] == drink_id
        ),
        None
    )

    data = {
        "title": "Напиток по ID",
        "drink_id": drink_id,
        "drink": drink,
    }

    return render(request, "drinks/drink_id.html", data)


def drink_by_slug(request, drink_slug):
    drink = next(
        (
            drink
            for drink in drinks_db
            if drink["slug"] == drink_slug
        ),
        None
    )

    data = {
        "title": "Страница напитка",
        "drink_slug": drink_slug,
        "drink": drink,
    }

    return render(request, "drinks/drink_slug.html", data)


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