# Generated by Django 4.2.14 on 2024-07-19 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_uploadedfile_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StockData',
        ),
    ]