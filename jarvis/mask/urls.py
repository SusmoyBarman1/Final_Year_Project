from django.urls import path
from . import views

urlpatterns = [
    path('', views.mask, name='mask'),
    path('/maskUpload', views.maskUpload, name='maskUpload'),
]