# Generated by Django 3.2.8 on 2021-11-26 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0004_auto_20211122_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='userenglish',
            name='changed_lang',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userenglish',
            name='query_lang',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]