# Generated by Django 4.2.1 on 2023-05-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0019_delete_article_delete_publication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('publications', models.ManyToManyField(to='table_data.publication')),
            ],
        ),
    ]
