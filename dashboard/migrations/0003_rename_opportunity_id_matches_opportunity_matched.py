# Generated by Django 3.2.2 on 2021-10-14 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_matches_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matches',
            old_name='opportunity_id',
            new_name='opportunity_matched',
        ),
    ]
