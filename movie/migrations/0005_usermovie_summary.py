# Generated by Django 3.2.8 on 2021-11-05 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_rename_creted_at_usermovie_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermovie',
            name='summary',
            field=models.CharField(default='感想・要約が入力されていません', max_length=150),
        ),
    ]
