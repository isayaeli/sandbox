# Generated by Django 3.2.9 on 2022-01-27 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_remove_matches_opportunity_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matches',
            name='startup',
        ),
    ]
