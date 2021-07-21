from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='search'),
    # path('', views.home, name='home'),
]