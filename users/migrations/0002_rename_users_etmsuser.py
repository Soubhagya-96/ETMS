# Generated by Django 5.1.6 on 2025-02-09 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='EtmsUser',
        ),
    ]
