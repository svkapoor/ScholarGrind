from django.urls import path
from . import views

app_name = 'study_groups'  # allows {% url 'studygroups:home' %} in templates

urlpatterns = [
    path('', views.studygroup_home, name='home'),  # URL: /studygroups/
]
