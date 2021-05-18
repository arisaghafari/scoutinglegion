# Generated by Django 3.1.7 on 2021-05-18 20:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hichhike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator_type', models.CharField(choices=[('d', 'راننده'), ('p', 'مسافر')], max_length=1)),
                ('creator_gender', models.CharField(choices=[('m', 'اقا'), ('f', 'خانوم')], max_length=1)),
                ('creator_age', models.IntegerField()),
                ('source', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('fellow_traveler_num', models.IntegerField()),
                ('description', models.TextField()),
                ('cities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('trip_time', models.DateTimeField()),
            ],
        ),
    ]
