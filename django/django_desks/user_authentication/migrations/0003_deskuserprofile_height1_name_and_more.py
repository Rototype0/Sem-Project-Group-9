# Generated by Django 4.2.17 on 2024-12-30 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0002_rename_height_deskuserprofile_height_cm_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deskuserprofile',
            name='height1_name',
            field=models.CharField(default='Default', max_length=50),
        ),
        migrations.AddField(
            model_name='deskuserprofile',
            name='height2_name',
            field=models.CharField(default='Default', max_length=50),
        ),
        migrations.AddField(
            model_name='deskuserprofile',
            name='height3_name',
            field=models.CharField(default='Default', max_length=50),
        ),
        migrations.AddField(
            model_name='deskuserprofile',
            name='height4_name',
            field=models.CharField(default='Default', max_length=50),
        ),
        migrations.AddField(
            model_name='deskuserprofile',
            name='height5_name',
            field=models.CharField(default='Default', max_length=50),
        ),
        migrations.AddField(
            model_name='deskuserprofile',
            name='height6_name',
            field=models.CharField(default='Default', max_length=50),
        ),
    ]
