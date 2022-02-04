from django.db import models


class UserBook(models.Model):
    title = models.CharField(max_length=50)
    itemUrl = models.CharField(max_length=100)
    ImageUrl = models.CharField(max_length=50)
    salesDate = models.CharField(max_length=15)
    vote_rate = models.CharField(default="評価なし", max_length=2)
    summary = models.CharField(default="感想・要約が入力されていません", max_length=150)
    auther = models.CharField(max_length=30)
    user_id = models.IntegerField()
    # tagといいねもつけたい
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class BookAPI(models.Model):
    ImageUrl = models.CharField(max_length=50)
    item_Url = models.CharField(max_length=50)
    book_id = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
