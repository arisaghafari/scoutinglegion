# Generated by Django 3.1.7 on 2021-04-18 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('latitude', 'longitude')},
        ),
    ]
