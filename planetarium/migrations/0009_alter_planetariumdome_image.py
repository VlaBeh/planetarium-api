# Generated by Django 5.1.2 on 2024-10-16 22:37

import planetarium.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0008_planetariumdome_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planetariumdome',
            name='image',
            field=models.ImageField(null=True, upload_to=planetarium.models.planetariumdome_image_path),
        ),
    ]