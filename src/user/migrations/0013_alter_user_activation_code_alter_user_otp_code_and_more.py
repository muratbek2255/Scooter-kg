# Generated by Django 4.0.6 on 2022-08-09 13:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_remove_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_code',
            field=models.CharField(blank=True, max_length=58),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_code',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_code_expiry',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]