# Generated by Django 3.2.2 on 2021-11-12 18:28

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0004_alter_talent_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talent',
            name='slug',
            field=models.SlugField(default=django.contrib.auth.models.User, unique=True),
        ),
    ]
