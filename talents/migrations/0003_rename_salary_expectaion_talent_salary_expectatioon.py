# Generated by Django 3.2.2 on 2021-11-12 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0002_alter_talent_experince'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talent',
            old_name='salary_expectaion',
            new_name='salary_expectatioon',
        ),
    ]
