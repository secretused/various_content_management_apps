from django.urls import path, include
from . import views

app_name = "idea"
urlpatterns = [
    # Homeに戻るようにnameで固定化
    path("", views.idea_home, name="idea_home"),
    path("save_idea/", views.save_idea, name="save_idea"),
    path('user_idea/<int:idea_id>/', views.user_idea, name='user_idea'),
    path("idea_edit/", views.idea_edit, name="idea_edit"),
]
