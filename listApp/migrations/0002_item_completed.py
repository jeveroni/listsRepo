# Generated by Django 4.2.14 on 2024-08-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]