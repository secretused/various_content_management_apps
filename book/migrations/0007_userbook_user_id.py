# Generated by Django 3.2.8 on 2021-11-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_userbook_vote_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
