from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError

from planet_api import settings
from user.models import User


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(ShowTheme, related_name="show_theme")

    def __str__(self):
        return f"{self.title} - {self.description} - {self.show_theme}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, related_name="sessions_ast", on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, related_name="sessions_pl", on_delete=models.CASCADE)
    show_time = models.DateTimeField('%H:%M')

    def __str__(self):
        return f"{self.astronomy_show.title} at {self.show_time} in {self.planetarium_dome}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, related_name="tickets", on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name="tickets_reserv", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('row', 'seat', 'show_session')

    def __str__(self):
        return f"Row: {self.row}, Seat: {self.seat}, {self.reservation}"

    def clean(self):
        planetarium_dome = self.show_session.planetarium_dome
        if not (1 <= self.row <= planetarium_dome.rows):
            raise ValidationError(f"Row must be between 1 and {planetarium_dome.rows}")
        if not (1 <= self.seat <= planetarium_dome.seats_in_row):
            raise ValidationError(f"Seat must be between 1 and {planetarium_dome.seats_in_row}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)