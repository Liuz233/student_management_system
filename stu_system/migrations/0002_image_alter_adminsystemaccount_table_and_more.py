# Generated by Django 5.0.6 on 2024-06-18 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stu_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='img')),
                ('student_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelTable(
            name='adminsystemaccount',
            table='adminsystemaccount',
        ),
        migrations.AlterModelTable(
            name='stusystemstudentaccount',
            table='stusystemstudentaccount',
        ),
    ]
