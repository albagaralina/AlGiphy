# Generated by Django 4.1.4 on 2024-06-06 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giphy_emails', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='sender',
        ),
    ]