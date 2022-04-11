# Generated by Django 3.2.2 on 2022-02-07 10:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0013_startup_rating'),
        ('dashboard', '0026_remove_matches_opportunity_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_opportunity', models.CharField(max_length=100)),
                ('date_paid', models.DateTimeField(default=datetime.datetime.now)),
                ('the_startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startups.startup')),
            ],
        ),
    ]
