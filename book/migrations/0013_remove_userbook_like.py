# Generated by Django 3.2.8 on 2021-12-09 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_userbook_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='like',
        ),
    ]