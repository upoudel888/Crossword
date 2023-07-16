from django.urls import path,include
from . import views

urlpatterns = [
    path("", view = views.welcome, name="welcome"),
    path("grid/", view = views.getGrid, name="grid")
]