# Generated by Django 3.2.6 on 2021-08-18 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['id']},
        ),
    ]
