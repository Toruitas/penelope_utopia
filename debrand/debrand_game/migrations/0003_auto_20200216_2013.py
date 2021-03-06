# Generated by Django 3.0.3 on 2020-02-16 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debrand_game', '0002_auto_20200216_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameobject',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
