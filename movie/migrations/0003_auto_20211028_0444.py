# Generated by Django 3.2.8 on 2021-10-28 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20211028_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('poster_path', models.CharField(max_length=50)),
                ('release_date', models.CharField(max_length=10)),
                ('auther', models.CharField(max_length=30)),
                ('creted_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]