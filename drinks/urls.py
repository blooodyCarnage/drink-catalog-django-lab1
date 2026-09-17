from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter


register_converter(FourDigitYearConverter, "year4")


urlpatterns = [
    path("", views.index, name="home"),

    path("about/", views.about, name="about"),


    path(
        "add-plain/",
        views.add_plain,
        name="add_plain"
    ),

    path(
        "add-model/",
        views.add_model,
        name="add_model"
    ),

    path("drinks/", views.drinks_list, name="drinks"),

    path(
        "category/<slug:cat_slug>/",
        views.show_category,
        name="category"
    ),
    path(
        "upload-file/",
        views.upload_file,
        name="upload_file"
    ),

    path(
        "tag/<slug:tag_slug>/",
        views.show_tag,
        name="tag"
    ),

    path(
        "drinks/<int:drink_id>/",
        views.drink_by_id,
        name="drink_id"
    ),

    path(
        "drinks/<slug:drink_slug>/",
        views.drink_by_slug,
        name="drink_slug"
    ),

    path(
        "search/",
        views.search,
        name="search"
    ),

    path(
        "archive/<year4:year>/",
        views.archive,
        name="archive"
    ),

    path(
        "go-home/",
        views.go_home,
        name="go_home"
    ),
]