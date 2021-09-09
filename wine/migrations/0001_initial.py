# Generated by Django 3.2.6 on 2021-09-09 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('delete_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=200)),
                ('reward_points', models.IntegerField(default=0)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
