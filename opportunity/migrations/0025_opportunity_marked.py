# Generated by Django 3.2.9 on 2022-01-19 13:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opportunity', '0024_alter_skills_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='marked',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
