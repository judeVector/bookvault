# Generated by Django 5.1.1 on 2024-09-18 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_created_at_user_date_joined'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_joined',
            new_name='created_at',
        ),
    ]
