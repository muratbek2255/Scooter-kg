# Generated by Django 4.0.6 on 2022-07-29 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]