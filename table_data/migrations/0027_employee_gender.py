# Generated by Django 4.2.1 on 2023-06-07 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0026_alter_department_dep_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=15, null=True),
        ),
    ]
