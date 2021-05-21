# Generated by Django 3.1.7 on 2021-05-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='name')),
                ('latitude', models.FloatField(verbose_name='location latitude')),
                ('longitude', models.FloatField(verbose_name='location longitude')),
                ('city', models.CharField(max_length=100, verbose_name='city of location')),
                ('state', models.CharField(max_length=100, verbose_name='state of location')),
                ('image', models.ImageField(blank=True, null=True, upload_to='Uploaded/location_picture', verbose_name='location picture')),
                ('description', models.TextField(blank=True, null=True, verbose_name='location description')),
                ('address', models.CharField(max_length=200, verbose_name='location address')),
                ('is_private', models.BooleanField(default=False, verbose_name='is private location')),
            ],
        ),
    ]
