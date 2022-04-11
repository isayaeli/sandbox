# Generated by Django 3.2.9 on 2022-01-06 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0008_startup'),
        ('opportunity', '0021_alter_opportunity_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='startup_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='startups.startup'),
        ),
    ]