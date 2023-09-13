from django.urls import path
import accounts.views as view

urlpatterns = [
    path("signup/", view.SignUpView.as_view(), name="signup"),
]
