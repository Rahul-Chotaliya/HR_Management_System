# Generated by Django 4.2.1 on 2023-05-17 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('table_data', '0009_publisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('pages', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rating', models.FloatField()),
                ('pubdate', models.DateField()),
                ('authors', models.ManyToManyField(to='table_data.author')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table_data.publisher')),
            ],
        ),
    ]
