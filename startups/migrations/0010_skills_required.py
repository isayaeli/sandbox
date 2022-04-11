# Generated by Django 3.2.9 on 2022-01-07 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('startups', '0009_auto_20220107_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills_Required',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startups.startup')),
            ],
            options={
                'verbose_name_plural': 'Skills_Required',
            },
        ),
    ]