from django.urls import path
from . import views

app_name = 'study_groups'  # allows {% url 'studygroups:home' %} in templates

urlpatterns = [
    path('', views.home, name='home'),  # URL: /studygroups/
    path('create/', views.create_group, name='create'),  # URL: /studygroups/create/
    path('join/<int:group_id>/', views.join_group, name='join'),
]
