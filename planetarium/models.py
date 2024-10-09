from django.db import models
from user.models import User


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)
    astronomy_show = models.ForeignKey(AstronomyShow, related_name="themes", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, related_name="sessions_ast", on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, related_name="sessions_pl", on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show.title} at {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by {self.user.username} on {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, related_name="tickets", on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, related_name="tickets_re", on_delete=models.CASCADE)

    def __str__(self):
        return f"Row {self.row}, Seat {self.seat}"
