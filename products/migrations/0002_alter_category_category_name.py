# Generated by Django 5.1.4 on 2024-12-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
