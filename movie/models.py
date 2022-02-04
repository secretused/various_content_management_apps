from django.db import models


class UserMovie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=50)
    poster_path = models.CharField(max_length=50)
    release_date = models.CharField(max_length=10)
    vote_rate = models.CharField(default="評価なし", max_length=2)
    summary = models.CharField(default="感想・要約が入力されていません", max_length=150)
    auther = models.CharField(max_length=30)
    user_id = models.IntegerField()
    # tagといいねもつけたい
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
