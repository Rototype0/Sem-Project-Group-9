# Generated by Django 5.1.4 on 2024-12-30 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authentication', '0003_deskuserprofile_height1_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='deskuserprofile',
            name='current_selected_desk_mac_address',
            field=models.CharField(default='cd:fb:1a:53:fb:e6', max_length=50),
        ),
    ]
