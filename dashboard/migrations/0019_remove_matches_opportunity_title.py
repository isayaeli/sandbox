# Generated by Django 3.2.9 on 2022-01-27 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_matches_talent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matches',
            name='opportunity_title',
        ),
    ]
