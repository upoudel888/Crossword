from django.urls import path,include
from . import views

urlpatterns = [
    path("", view = views.solve, name="Solver")
]