# Generated by Django 3.1.7 on 2021-04-28 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0003_auto_20210418_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(verbose_name='location latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(verbose_name='location longitude'),
        ),
    ]
