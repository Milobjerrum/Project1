"""Django Module"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("<str:titel>/", views.entry, name="view_entry"),
    path("wiki/<str:titel>/", views.entry, name="view_wiki/entry"),
    path("edit", views.edit, name="edit"),
    path("random", views.view_random, name="random")

]
