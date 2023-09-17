from django.urls import path
from .import views

urlpatterns = [
    path('index/',views.mainPage , name="index"),
    path('likepost',views.like_post,name="likepost"),
    path('deletepost',views.delete_post,name="deletepost"),
    ]