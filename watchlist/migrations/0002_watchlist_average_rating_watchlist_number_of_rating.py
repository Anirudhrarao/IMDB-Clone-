# Generated by Django 5.0.2 on 2024-03-16 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='average_rating',
            field=models.FloatField(default=0, verbose_name='Average rating'),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_of_rating',
            field=models.IntegerField(default=0, verbose_name='Number of rating'),
        ),
    ]
