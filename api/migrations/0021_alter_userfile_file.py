# Generated by Django 5.2 on 2025-05-31 23:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0020_alter_userfile_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfile",
            name="file",
            field=models.FileField(max_length=255, upload_to="uploads/"),
        ),
    ]
