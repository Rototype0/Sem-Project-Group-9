# Generated by Django 5.1.2 on 2024-12-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Desk',
            fields=[
                ('mac_address', models.CharField(max_length=17, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('state_data', models.JSONField(default=dict)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
