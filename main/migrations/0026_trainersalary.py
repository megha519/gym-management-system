# Generated by Django 5.0.6 on 2024-07-24 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_trainerachivement'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt', models.IntegerField()),
                ('amt_date', models.DateField()),
                ('remarks', models.TextField(blank=True)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.trainer')),
            ],
            options={
                'verbose_name_plural': 'Trainer Salary',
            },
        ),
    ]