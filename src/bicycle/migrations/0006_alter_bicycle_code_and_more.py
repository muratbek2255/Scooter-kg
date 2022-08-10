# Generated by Django 4.0.6 on 2022-08-05 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bicycle', '0005_alter_bicycle_code_alter_bicycle_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicycle',
            name='code',
            field=models.CharField(blank=True, default='1HHN89FD', max_length=255, unique=True, verbose_name='КОд'),
        ),
        migrations.AlterField(
            model_name='ratingbicyclerelation',
            name='bicycle',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rating_bicycles', to='bicycle.bicycle', verbose_name='Велосипед'),
        ),
        migrations.AlterField(
            model_name='ratingbicyclerelation',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rating_users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
