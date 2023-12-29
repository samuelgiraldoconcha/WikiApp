from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("samuel", views.Samuel, name="Samuel"),
    path("wiki/random", views.random_entry, name="random"),
    path("wiki/modify/<str:title>", views.modify_entry, name="modify_entry"),
    path("wiki/search", views.search_results, name="search_results"),
    path("wiki/new_entry", views.create_new_entry, name="new_entry"),
    path("wiki/<str:TITLE>", views.display_entries, name="display_entries"),
]
