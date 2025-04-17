# Generated by Django 5.1.6 on 2025-04-17 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('Street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('country', models.CharField(default='Canada', max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone_number', models.CharField(max_length=15, unique=True)),
                ('type_client', models.BooleanField(default=False)),
                ('report_sent', models.BooleanField(default=False)),
                ('date_report_sent', models.DateField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
