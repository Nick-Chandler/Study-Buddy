# Generated by Django 5.2 on 2025-05-30 18:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0016_alter_threadmessage_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="threadmessage",
            old_name="id",
            new_name="message_id",
        ),
    ]
