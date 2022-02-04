# Generated by Django 3.2.8 on 2021-11-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('ImageUrl', models.CharField(max_length=50)),
                ('salesDate', models.CharField(max_length=15)),
                ('reviewAverage', models.CharField(max_length=30)),
                ('summary', models.CharField(max_length=150)),
                ('auther', models.CharField(max_length=30)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]