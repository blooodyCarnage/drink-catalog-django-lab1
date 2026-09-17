from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("drinks.urls")),
]


admin.site.site_header = 'Панель управления каталогом напитков'
admin.site.site_title = 'Каталог напитков'
admin.site.index_title = 'Управление напитками и связанными данными'


handler404 = "drinks.views.page_not_found"