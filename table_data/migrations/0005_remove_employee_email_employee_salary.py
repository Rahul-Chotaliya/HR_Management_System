# Generated by Django 4.2.1 on 2023-05-16 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0004_employee_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
