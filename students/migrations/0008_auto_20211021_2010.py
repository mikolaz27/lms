# Generated by Django 3.2.7 on 2021-10-21 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0007_auto_20211021_1951"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="room",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="courses",
                to="students.room",
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="students",
                to="students.course",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="course",
            field=models.ManyToManyField(related_name="teachers", to="students.Course"),
        ),
    ]