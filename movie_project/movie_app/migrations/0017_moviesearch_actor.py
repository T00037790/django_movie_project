# Generated by Django 2.2.2 on 2019-06-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0016_auto_20190614_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviesearch',
            name='actor',
            field=models.ManyToManyField(to='movie_app.Actor'),
        ),
    ]
