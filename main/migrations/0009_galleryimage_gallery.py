# Generated by Django 5.0.6 on 2024-06-09 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_gallery_galleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='gallery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.gallery'),
        ),
    ]