# Generated by Django 3.2.9 on 2022-01-21 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talents', '0015_skill_experience'),
        ('dashboard', '0015_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent'),
        ),
    ]