# Generated by Django 3.2.8 on 2021-11-29 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_alter_user_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(default='https://cdn2.aprico-media.com/production/imgs/images/000/029/940/original.png?1553946576', upload_to='images/', verbose_name='user_image'),
        ),
    ]
