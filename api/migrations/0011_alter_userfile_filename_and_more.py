# Generated by Django 5.2 on 2025-05-28 18:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0010_alter_userfile_filename"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="userfile",
            name="filename",
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name="userfile",
            constraint=models.UniqueConstraint(
                fields=("user", "filename"), name="unique_filename_per_user"
            ),
        ),
    ]
