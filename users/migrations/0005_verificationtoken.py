# Generated by Django 5.1.6 on 2025-03-02 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_comments_id_alter_etmsuser_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=128, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.etmsuser')),
            ],
        ),
    ]
