# Generated by Django 5.1 on 2024-09-08 20:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_socialmedia_usersocialmedia_idsocialmedia_and_more'),
        ('roadMap', '0004_rename_checked_checkpoint_completed_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='roadmap',
            old_name='username',
            new_name='idUser',
        ),
        migrations.CreateModel(
            name='LikeRoadmap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idRoadmap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadMap.roadmap')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.person')),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idInterest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadMap.interest')),
                ('idUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
