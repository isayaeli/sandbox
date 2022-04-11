# Generated by Django 3.2.2 on 2021-10-14 05:52

import datetime
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
            name='Matches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opportunity_id', models.CharField(max_length=255)),
                ('matched_on', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[('shortlisted', 'shortlisted'), ('rejected', 'rejected'), ('reviewing', 'reviewing'), ('interviewed', 'interviewed'), ('offergiven', 'offergiven')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
    ]