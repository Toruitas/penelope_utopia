# Generated by Django 3.0.3 on 2020-02-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debrand_game', '0003_auto_20200216_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='img_src',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
