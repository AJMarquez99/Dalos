from typing import Any
from django import http
from django.db import models
from django.views.generic import View, TemplateView, CreateView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from .admin import UserCreationForm


from pages.plotly_apps import createStockDash
import yfinance as yf
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from .stock_data import StockPage

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {"sticky": True}

class TickerPageView(TemplateView):
    template_name = "ticker.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ticker = StockPage(yf.Ticker(self.kwargs["ticker"]))
        return {"ticker" : ticker,
                "dashApp": ticker.symbol + 'App'}
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        request.user.is_authenticated
        createStockDash(yf.Ticker(kwargs["ticker"]), request.user.is_authenticated)

        dash_context = request.session.get("django_plotly_dash", dict())
        dash_context['django_to_dash_context'] = "I am Dash recieving context from Django"
        request.session['django_plotly_dash'] = dash_context
        return super().setup(request, *args, **kwargs)
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("lazy")
    template_name = "registration/signup.html"

class ProfileView(TemplateView):
    template_name = "profile.html"

def search_bar(request):
  response = HttpResponse(status=302)
  ticker = request.GET['search']

  if len(yf.Ticker(ticker).history(period='7d')) > 0:
      response['Location'] = '/ticker/' + ticker
  else:
      response['Location'] = ''
  
  return response