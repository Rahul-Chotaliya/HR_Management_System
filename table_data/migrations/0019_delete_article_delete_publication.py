# Generated by Django 4.2.1 on 2023-05-19 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0018_publication_article'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Publication',
        ),
    ]
