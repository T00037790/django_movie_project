# Generated by Django 2.2.2 on 2019-06-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0002_auto_20190607_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default=None, upload_to='static/movie_app/posters'),
        ),
    ]