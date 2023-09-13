from django.urls import path
import pages.views as view

urlpatterns = [
    
    path(r'search', view.search_bar, name="search"),
    path("", view.HomePageView.as_view(), name="home"),
    path("ticker/<str:ticker>", view.TickerPageView.as_view(), name="ticker"),
    path("signup/", view.SignUpView.as_view(), name="signup"),
]