# Generated by Django 5.1 on 2024-09-08 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roadMap', '0005_rename_username_roadmap_iduser_likeroadmap_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkpoint',
            old_name='idRoadmap',
            new_name='roadmap',
        ),
        migrations.RenameField(
            model_name='likeroadmap',
            old_name='idRoadmap',
            new_name='roadmap',
        ),
        migrations.RenameField(
            model_name='likeroadmap',
            old_name='idUser',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='roadmap',
            old_name='idInterest',
            new_name='interest',
        ),
        migrations.RenameField(
            model_name='roadmap',
            old_name='idUser',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userinterest',
            old_name='idInterest',
            new_name='interest',
        ),
        migrations.RenameField(
            model_name='userinterest',
            old_name='idUser',
            new_name='user',
        ),
    ]
