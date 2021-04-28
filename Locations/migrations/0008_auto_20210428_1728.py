# Generated by Django 3.1.7 on 2021-04-28 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Locations', '0007_auto_20210428_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='creator',
        ),
        migrations.AddField(
            model_name='location',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator_location', to=settings.AUTH_USER_MODEL),
        ),
    ]
