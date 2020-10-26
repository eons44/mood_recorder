from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createUserEmotion', views.create_user_emotion, name='create_user_emotion'),
    path('getUserEmotion', views.get_user_emotion, name='get_user_emotion'),
    path('getAllUserEmotions', views.get_all_user_emotions, name='get_user_emotion'),
]