from django.shortcuts import render

# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("lazy")
    template_name = "registration/signup.html"