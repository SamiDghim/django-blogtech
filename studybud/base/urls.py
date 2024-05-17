from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"), # (direct path, views, name)
    path('room/' , views.room, name='room'),
]
