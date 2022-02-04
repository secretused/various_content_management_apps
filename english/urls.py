from django.urls import path, include
from . import views

app_name = "english"
urlpatterns = [
    # Homeに戻るようにnameで固定化
    path("", views.get_youtube_data, name="get_youtube_data"),
    path("reload_ok", views.reload_data, name="reload_data"),
    path("translate/", views.translate, name="translate"),
    path("english_edit/", views.english_edit, name="english_edit"),
]
