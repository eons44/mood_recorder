from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createUserEmotion', views.create_user_emotion, name='create_user_emotion'),
    path('getUserEmotion/<int:user_id>/<str:emotion>', views.index),
]