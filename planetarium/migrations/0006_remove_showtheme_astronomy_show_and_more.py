# Generated by Django 5.1.2 on 2024-10-14 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0005_alter_ticket_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showtheme',
            name='astronomy_show',
        ),
        migrations.AddField(
            model_name='astronomyshow',
            name='show_theme',
            field=models.ManyToManyField(related_name='show_theme', to='planetarium.showtheme'),
        ),
    ]