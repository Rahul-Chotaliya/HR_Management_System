# Generated by Django 4.2.1 on 2023-05-16 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0006_employee_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='FullName',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]