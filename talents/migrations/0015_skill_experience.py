# Generated by Django 3.2.9 on 2022-01-20 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0014_alter_experience_finish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='experience',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
