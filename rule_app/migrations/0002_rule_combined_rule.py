# Generated by Django 5.1.2 on 2024-10-26 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rule_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='combined_rule',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
