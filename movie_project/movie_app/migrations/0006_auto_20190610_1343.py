# Generated by Django 2.2.2 on 2019-06-10 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0005_auto_20190609_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default=None, upload_to='movie_app/posters'),
        ),
    ]
