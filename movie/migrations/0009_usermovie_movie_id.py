# Generated by Django 3.2.8 on 2021-11-23 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_usermovie_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermovie',
            name='movie_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
