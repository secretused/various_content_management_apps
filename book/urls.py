from django.urls import path, include
from . import views

app_name = "book"
urlpatterns = [
    # Homeに戻るようにnameで固定化
    path("", views.saved_book, name="saved_book"),
    path("user_books/", views.search_books, name="search_books"),
    path("reload_ok", views.reload_data, name="reload_data"),
    path("save_book/", views.user_book, name="user_book"),
    path("edit_book/", views.edit_book, name="edit_book"),
    path("mypage_edit_book/", views.mypage_edit_book, name="mypage_edit_book"),
    path("mypage_delete_book/", views.mypage_delete_book,
         name="mypage_delete_book"),
]
