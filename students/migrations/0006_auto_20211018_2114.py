# Generated by Django 3.2.7 on 2021-10-18 18:14

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_alter_course_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True),
        ),
    ]
