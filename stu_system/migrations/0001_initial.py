# Generated by Django 5.0.6 on 2024-06-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAccount',
            fields=[
                ('student_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('stu_name', models.CharField(max_length=20)),
                ('stu_password', models.CharField(max_length=20)),
            ],
        ),
    ]