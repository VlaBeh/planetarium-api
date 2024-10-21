from multiprocessing.connection import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from planetarium.models import Ticket, ShowSession, Reservation, AstronomyShow, PlanetariumDome
from planetarium.serializers import TicketSerializer

TICKET_URL = reverse("planetarium:ticket-list")


def sample_show_session(**params) -> ShowSession:
    astronomy_show = AstronomyShow.objects.create(
        title="Sample Show",
        description="Sample description"
    )
    planetarium_dome = PlanetariumDome.objects.create(
        name="Sample Dome",
        rows=10,
        seats_in_row=30
    )
    defaults = {
        "astronomy_show": astronomy_show,
        "planetarium_dome": planetarium_dome,
        "show_time": "2024-10-21",
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def sample_reservation(**params) -> Reservation:
    defaults = {
        "user": get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        ),
    }
    defaults.update(params)
    return Reservation.objects.create(**defaults)


def sample_ticket(**params) -> Ticket:
    show_session = ShowSession.objects.first()
    reservation = Reservation.objects.first()

    defaults = {
        "row": 2,
        "seat": 23,
        "show_session": show_session,
        "reservation": reservation,
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)


class UnauthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TICKET_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_ticket_list(self):
        sample_ticket()

        response = self.client.get(TICKET_URL)
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(response.data["results"], serializer.data)
