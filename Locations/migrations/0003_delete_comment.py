# Generated by Django 3.1.13 on 2021-07-06 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Locations', '0002_auto_20210706_2355'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]