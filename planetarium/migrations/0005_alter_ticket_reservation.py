# Generated by Django 5.1.2 on 2024-10-13 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0004_alter_ticket_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets_reserv', to='planetarium.reservation'),
        ),
    ]