# Generated by Django 3.2.8 on 2021-11-02 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='reviewAverage',
        ),
    ]