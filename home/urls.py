from django.urls import path
from . import views
from home.dash_apps import omr

urlpatterns = [
    path('', views.home, name='home')
]