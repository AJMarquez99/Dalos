from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.http import HttpRequest
from typing import Any

from django.contrib.auth.decorators import login_required

from .models import *
from .stock_class import StockPage
from .plotly_apps import createStockDash

class HomeView(TemplateView):
  template_name = 'pages/index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['segment'] = 'index'
    return context
  
class StockView(TemplateView):
  template_name = 'pages/ticker.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['segment'] = 'stock'

    ticker = StockPage(self.kwargs["ticker"])
    context["stock"] = ticker.stockInfo
    context["dashApp"] = ticker.stockInfo.symbol + "App"
    return context
  
  def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
    request.user.is_authenticated
    createStockDash(kwargs["ticker"], request.user.is_authenticated)

    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['django_to_dash_context'] = "I am Dash recieving context from Django"
    request.session['django_plotly_dash'] = dash_context
    return super().setup(request, *args, **kwargs)


def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)
