# Generated by Django 3.2.7 on 2021-10-18 17:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0004_alter_course_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
