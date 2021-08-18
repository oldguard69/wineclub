# Generated by Django 3.2.6 on 2021-08-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_book_options'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='cart',
            name='books',
            field=models.ManyToManyField(through='cart.CartItem', to='book.Book'),
        ),
    ]
