from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"), # (direct path, views, name)
    path('room/<str:pk>/' , views.room, name='room'), # we add name to access to url by name

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room")
]
