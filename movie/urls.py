from django.urls import path, include
from . import views

app_name = "movie"
urlpatterns = [
    # Homeに戻るようにnameで固定化
    path("", views.saved_movie, name="saved_movie"),
    path("user_movies/", views.search_movies, name="search_movies"),
    path("save_movie/", views.user_movie, name="user_movie"),
    path("edit_movie/", views.edit_movie, name="edit_movie"),
    path("mypage_edit_movie/", views.mypage_edit_movie, name="mypage_edit_movie"),
    path("mypage_delete_movie/", views.mypage_delete_movie,
         name="mypage_delete_movie"),
    path("like=<int:id>/", views.like, name="like"),
]
