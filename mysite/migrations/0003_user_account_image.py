# Generated by Django 3.2.8 on 2021-10-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_image',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]