# Generated by Django 3.2.2 on 2022-02-27 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0032_package_payment_txt_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='package_payment',
            name='package_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='package_payment',
            name='amount_paid',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='package_payment',
            name='txt_ref',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='package_payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
