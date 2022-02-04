from django.db import models


class UserIdea(models.Model):

    user_id = models.IntegerField()
    username = models.CharField(max_length=30)
    idea_title = models.CharField(max_length=50)
    idea_detail = models.CharField(default="アイデアの詳細が入力されていません", max_length=300)
    idea_tag = models.CharField(default="タグが入力されていません", max_length=30)
    idea_from = models.CharField(default="思いついたきっかけが入力されていません", max_length=300)
    idea_for = models.CharField(default="アイデアの用途が入力されていません", max_length=300)
    idea_target = models.CharField(default="ターゲットが入力されていません", max_length=300)
    idea_price = models.IntegerField(default=0)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class ThreadComment(models.Model):

    user_id = models.IntegerField()
    username = models.CharField(max_length=30)
    account_image = models.ImageField(
        default="https://cdn2.aprico-media.com/production/imgs/images/000/029/940/original.png?1553946576", upload_to='images/', null=True)
    idea_id = models.IntegerField()
    comment = models.CharField(default="コメント無し", max_length=150)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
