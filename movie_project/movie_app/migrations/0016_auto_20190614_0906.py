# Generated by Django 2.2.2 on 2019-06-14 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0015_auto_20190614_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviesearch',
            name='actor',
        ),
        migrations.AddField(
            model_name='moviesearch',
            name='director',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movie_app.Director'),
        ),
    ]
