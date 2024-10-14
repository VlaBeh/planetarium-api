from django.db import models
from django.db.models import UniqueConstraint

from planet_api import settings
from user.models import User


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(ShowTheme, related_name="show_theme")

    def __str__(self):
        return self.title, self.description, self.show_theme


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, related_name="sessions_ast", on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, related_name="sessions_pl", on_delete=models.CASCADE)
    show_time = models.DateTimeField()

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
    reservation = models.ForeignKey(Reservation, related_name="tickets_reserv", on_delete=models.CASCADE,
                                    null=True, blank=True)

    class Meta:
        UniqueConstraint(fields=['row', 'seat', 'show_session'], name="unique_ticket")

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat}"

    def clean(self):
        if not (1 <= self.seat <= 40):
            raise ValueError("Seat must be between 1 and 40")
