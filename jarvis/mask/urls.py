from django.urls import path
from . import views

urlpatterns = [
    path('', views.mask, name='mask'),
    path('/maskdemo', views.maskdemo, name='maskdemo'),
    path('/add', views.add, name='add')
]