# Generated by Django 3.2.6 on 2021-08-19 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_book_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='quanity',
            new_name='quantity',
        ),
    ]