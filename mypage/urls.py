from django.urls import path, include
from . import views

app_name = "mypage"
urlpatterns = [
    # Homeに戻るようにnameで固定化
    path("", views.mypage, name="mypage"),
    path("my_edit/", views.profile_edit, name="profile_edit"),
    path("email_save/", views.profile_email_save, name="profile_email_save"),
    path("password_save/", views.profile_password_save,
         name="profile_password_save"),
    path("my_movie/", views.mypage_tab1, name="mypage_tab1"),
    path("my_book/", views.mypage_tab2, name="mypage_tab2"),
    path("my_idea/", views.mypage_tab3, name="mypage_tab3"),
    path("my_idea/", views.mypage_tab3, name="mypage_tab3"),
    path("my_idea/<int:idea_id>/", views.mypage_tab3_user, name="mypage_tab3_user"),
    path("my_english/", views.mypage_tab5, name="mypage_tab5"),
]
