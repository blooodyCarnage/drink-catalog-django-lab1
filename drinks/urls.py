from django.urls import path, register_converter

from . import views
from .converters import FourDigitYearConverter


register_converter(FourDigitYearConverter, "year4")


urlpatterns = [
    path(
        "",
        views.index,
        name="home"
    ),

    path(
        "about/",
        views.AboutView.as_view(),
        name="about"
    ),

    path(
        "add-plain/",
        views.AddDrink.as_view(),
        name="add_plain"
    ),

    path(
        "add-model/",
        views.CreateDrink.as_view(),
        name="add_model"
    ),

    path(
        "drinks/",
        views.DrinkListView.as_view(),
        name="drinks"
    ),

    path(
        "category/<slug:cat_slug>/",
        views.DrinkCategory.as_view(),
        name="category"
    ),

    path(
        "upload-file/",
        views.UploadFileView.as_view(),
        name="upload_file"
    ),

    path(
        "tag/<slug:tag_slug>/",
        views.DrinkTag.as_view(),
        name="tag"
    ),

    path(
        "drinks/<int:drink_id>/",
        views.drink_by_id,
        name="drink_id"
    ),

    path(
        "drinks/<slug:drink_slug>/edit/",
        views.UpdateDrink.as_view(),
        name="edit_drink"
    ),

    path(
        "drinks/<slug:drink_slug>/delete/",
        views.DeleteDrink.as_view(),
        name="delete_drink"
    ),

    path(
        "drinks/<slug:drink_slug>/",
        views.ShowDrink.as_view(),
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