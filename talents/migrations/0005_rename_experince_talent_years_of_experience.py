# Generated by Django 3.2.2 on 2021-11-12 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0004_rename_salary_expectatioon_talent_salary_expectation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talent',
            old_name='experince',
            new_name='years_of_experience',
        ),
    ]
