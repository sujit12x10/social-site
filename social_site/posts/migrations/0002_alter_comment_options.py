# Generated by Django 5.0.6 on 2024-06-24 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
    ]
