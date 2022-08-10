# Generated by Django 4.0.6 on 2022-08-09 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[('платеж получен', 'платеж получен'), ('платеж сделан', 'платеж сделан'), ('платеж снят', 'платеж снят'), ('платеж заполнен', 'платеж заполнен')], default='payment_made', max_length=64)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Dates')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='stripe_payment.wallet', verbose_name='Wallet')),
            ],
        ),
    ]
