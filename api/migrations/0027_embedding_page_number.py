# Generated by Django 5.2 on 2025-06-21 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0026_alter_userfile_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="embedding",
            name="page_number",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
