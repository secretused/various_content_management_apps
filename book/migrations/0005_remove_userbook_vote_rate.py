# Generated by Django 3.2.8 on 2021-11-05 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_userbook_vote_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='vote_rate',
        ),
    ]
