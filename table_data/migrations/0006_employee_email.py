# Generated by Django 4.2.1 on 2023-05-16 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0005_remove_employee_email_employee_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]