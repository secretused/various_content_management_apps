# Generated by Django 3.2.8 on 2021-11-23 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_userbook_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='itemUrl',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
