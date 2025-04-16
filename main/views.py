from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'main/home.html'

# Create your views here.
def home(request):
    return render(request, 'main/home.html')