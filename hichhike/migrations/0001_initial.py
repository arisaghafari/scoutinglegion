# Generated by Django 3.1.7 on 2021-06-06 12:36

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


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
                ('description', models.TextField(blank=True)),
                ('cities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('trip_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('hichhike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Participants_hichhike', to='hichhike.hichhike')),
            ],
        ),
    ]
