# Generated by Django 3.1.7 on 2021-05-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hichhike', '0002_hichhike_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hichhike',
            name='trip_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
