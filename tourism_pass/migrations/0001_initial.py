# Generated by Django 3.2.6 on 2021-09-09 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourismPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('delete_at', models.DateTimeField(null=True)),
                ('reward_points', models.IntegerField()),
                ('qr_code', models.UUIDField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('price', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=200)),
                ('is_bougth', models.BooleanField(default=False)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]