# Generated by Django 3.0.3 on 2020-02-17 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debrand_game', '0007_level_sidebar'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='img_attribution',
            field=models.CharField(blank=True, max_length=96),
        ),
    ]
