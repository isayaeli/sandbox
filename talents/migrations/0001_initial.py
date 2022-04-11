# Generated by Django 3.2.2 on 2021-11-12 18:53

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Talent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('about', models.TextField()),
                ('category', models.CharField(choices=[('Architecture & Construction', 'Architecture & Construction'), ('Accountancy and Financial Management', 'Accountancy and Financial Management'), ('Business, Consulting and Management', 'Business, Consulting and Management '), ('Law and Legal Services', 'Law and Legal Services'), ('Non Government Organization', 'Non Government Organization '), ('Media and Communications', 'Media and Communications'), ('Creative Arts and Design', 'Creative Arts and Design'), ('Energy and Utilities', 'Energy and Utilities'), ('Engineering and Manufacturing', 'Engineering and Manufacturing'), ('Agribusiness', 'Agribusiness'), ('Medical and Healthcare', 'Medical and Healthcare'), ('Information Technology', 'Information Technology'), ('Hospitality and Tourism', 'Hospitality and Tourism'), ('Marketing, Advertising and PR', 'Marketing, Advertising and PR'), ('Sales', 'Sales'), ('Real Estate', 'Real Estate'), ('Finance, Retail and Banking Services', 'Finance, Retail and Banking Services'), ('Office Management and Human Resources Services', 'Office Management and Human Resources Services'), ('Transportation, Distribution & Logistics', 'Transportation, Distribution & Logistics')], max_length=100)),
                ('experince', models.CharField(choices=[('Less than 1 Year', 'Less than 1 Year'), ('2 - 5 years', '2 - 5 years'), ('5 - 7 years', '5 - 7 years'), ('7 -10 years', '7 -10 years'), ('10 years and above', '10 years and above')], max_length=100)),
                ('dob', models.DateTimeField(default=datetime.datetime.now)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=10)),
                ('languages', models.CharField(max_length=100)),
                ('salary_expectaion', models.CharField(max_length=100)),
                ('prefered_work_type', models.CharField(choices=[('full time', 'full time'), ('remote', 'remote'), ('contractual', 'contractual'), ('internship', 'internship'), ('voluntering', 'voluntering'), ('freelance', 'freelance'), ('part-time', 'part-time'), ('temporary', 'temporary'), ('internship', 'internship')], max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('location', models.CharField(max_length=100)),
                ('linkedIn', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(default=django.contrib.auth.models.User, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('views', models.ManyToManyField(blank=True, related_name='views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('finish_date', models.DateTimeField(default=datetime.datetime.now)),
                ('position', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=datetime.datetime.now)),
                ('end_date', models.DateTimeField(max_length=100)),
                ('school_name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent')),
            ],
            options={
                'verbose_name_plural': 'Education',
            },
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('awarded_on', models.DateTimeField(default=datetime.datetime.now)),
                ('details', models.TextField()),
                ('talent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talents.talent')),
            ],
        ),
    ]
