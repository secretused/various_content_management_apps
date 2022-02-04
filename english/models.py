from django.db import models


class UserEnglish(models.Model):
    search_text = models.CharField(max_length=50)
    changed_text = models.CharField(max_length=50)
    query_lang = models.CharField(max_length=2)
    changed_lang = models.CharField(max_length=2)
    user_id = models.IntegerField()

    # checkbox
    checkbox_1 = models.CharField(max_length=10, default='unchecked')
    checkbox_2 = models.CharField(max_length=10, default='unchecked')
    checkbox_3 = models.CharField(max_length=10, default='unchecked')

    # tagといいねもつけたい
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class EnglishVideo(models.Model):
    thumbnails = models.CharField(max_length=50)
    link_url = models.CharField(max_length=50)
    video_id = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)
