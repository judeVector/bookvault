# Generated by Django 5.1.1 on 2024-09-17 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_book_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='borrowed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.user'),
        ),
        migrations.AddField(
            model_name='book',
            name='borrowed_until',
            field=models.DateField(blank=True, null=True),
        ),
    ]
