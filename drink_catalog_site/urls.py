from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include("drinks.urls")),

    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]


admin.site.site_header = 'Панель управления каталогом напитков'
admin.site.site_title = 'Каталог напитков'
admin.site.index_title = 'Управление напитками и связанными данными'


handler404 = "drinks.views.page_not_found"