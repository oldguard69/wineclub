# Generated by Django 3.2.6 on 2021-08-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField(blank=True)),
                ('password', models.CharField(max_length=200)),
                ('date_join', models.DateField(auto_now_add=True)),
                ('favorite_books', models.ManyToManyField(to='book.Book')),
            ],
        ),
    ]
