# Generated by Django 5.1 on 2024-08-15 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='ratings',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
    ]
