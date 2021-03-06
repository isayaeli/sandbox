# Generated by Django 3.2.2 on 2021-09-30 07:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='avatar.png', upload_to='profile_images')),
                ('genre', models.CharField(blank=True, max_length=100, null=True)),
                ('user_type', models.CharField(choices=[('not_set', 'not_set'), ('talent', 'talent'), ('startup', 'startup')], default='not_set', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
