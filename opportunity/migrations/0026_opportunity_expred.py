# Generated by Django 3.2.9 on 2022-01-24 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0025_opportunity_marked'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='expred',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10),
        ),
    ]
