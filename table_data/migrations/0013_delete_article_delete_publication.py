# Generated by Django 4.2.1 on 2023-05-18 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0012_publication_alter_store_books_article'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Publication',
        ),
    ]