# Generated by Django 4.2.1 on 2023-06-07 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0025_alter_department_dep_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dep_name',
            field=models.CharField(max_length=255, verbose_name='Department Name'),
        ),
    ]
