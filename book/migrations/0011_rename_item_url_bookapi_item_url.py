# Generated by Django 3.2.8 on 2021-11-25 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_rename_video_id_bookapi_book_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookapi',
            old_name='item_url',
            new_name='item_Url',
        ),
    ]
