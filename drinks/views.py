from django.http import (
    HttpResponse,
    HttpResponseNotFound
)
from django.shortcuts import redirect


def index(request):
    return HttpResponse(
        "<h1>Каталог напитков</h1>"
        "<p>Добро пожаловать в каталог напитков.</p>"
        "<p>Здесь представлены различные виды напитков.</p>"
    )


def drinks_list(request):
    return HttpResponse(
        "<h1>Каталог напитков</h1>"
        "<ul>"
        "<li>Кола</li>"
        "<li>Апельсиновый сок</li>"
        "<li>Минеральная вода</li>"
        "<li>Холодный чай</li>"
        "</ul>"
    )


def drink_by_id(request, drink_id):
    return HttpResponse(
        f"<h2>Напиток по ID</h2>"
        f"<p>drink_id = {drink_id}</p>"
    )


def drink_by_slug(request, drink_slug):
    return HttpResponse(
        f"<h2>Страница напитка</h2>"
        f"<p>slug = {drink_slug}</p>"
    )


def search(request):
    drink_type = request.GET.get("type", "")
    brand = request.GET.get("brand", "")

    print(request.GET)

    return HttpResponse(
        "<h2>Поиск напитков</h2>"
        f"<p>type = {drink_type}</p>"
        f"<p>brand = {brand}</p>"
    )


def archive(request, year):
    if year > 2026:
        return redirect("home")

    return HttpResponse(
        f"<h2>Архив каталога</h2>"
        f"<p>Год: {year}</p>"
    )


def go_home(request):
    return redirect("home")


def page_not_found(request, exception):
    return HttpResponseNotFound(
        "<h1>404</h1>"
        "<p>Страница не найдена</p>"
    )