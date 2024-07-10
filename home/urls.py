from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as view

urlpatterns = [
  path('', view.HomeView.as_view(),  name='index'),
  path("ticker/<str:ticker>", view.StockView.as_view(), name="stock"),
  path('tables/', view.tables, name='tables'),
]
