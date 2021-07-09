# Generated by Django 3.1.13 on 2021-07-09 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user_rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Urate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator_location', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='location',
            name='kinds',
            field=models.ManyToManyField(related_name='location', to='Locations.Category'),
        ),
        migrations.AddField(
            model_name='comment',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Locations.location'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user_rate', 'location')},
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('latitude', 'longitude')},
        ),
    ]
