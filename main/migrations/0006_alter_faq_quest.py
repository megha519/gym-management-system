# Generated by Django 5.0.6 on 2024-06-08 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='quest',
            field=models.CharField(max_length=200),
        ),
    ]