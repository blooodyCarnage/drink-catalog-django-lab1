from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("drinks.urls")),
]


handler404 = "drinks.views.page_not_found"