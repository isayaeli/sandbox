# Generated by Django 3.2.2 on 2021-06-25 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='opportunity',
            options={'verbose_name_plural': 'Opportunities'},
        ),
        migrations.AddField(
            model_name='opportunity',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
