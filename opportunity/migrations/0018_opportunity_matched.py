# Generated by Django 3.2.2 on 2021-10-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0017_remove_opportunity_matches'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='matched',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
