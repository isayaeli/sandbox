# Generated by Django 3.2.2 on 2021-10-07 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0011_opportunity_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opportunity',
            name='status',
        ),
    ]
