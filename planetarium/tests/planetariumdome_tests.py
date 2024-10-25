from multiprocessing.connection import Client
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from planetarium.models import Ticket, ShowSession, Reservation, AstronomyShow, PlanetariumDome
from planetarium.serializers import TicketSerializer, TicketListSerializer, TicketRetrieveSerializer

TICKET_URL = reverse("planetarium:ticket-list")

PLANETARIUMDOME_URL = reverse("planetarium:planetariumdome-list")


def detail_url(ticket_id):
    return reverse("planetarium:ticket-detail", kwargs={"pk": ticket_id})


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
    try:
        user = get_user_model().objects.get(email="test@test.com")
    except ObjectDoesNotExist:
        user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpass"
        )

    defaults = {
        "user": user,
    }
    defaults.update(params)
    return Reservation.objects.create(**defaults)


def sample_ticket(**params) -> Ticket:
    # Створюємо сесію, якщо її ще немає
    show_session = ShowSession.objects.first() or sample_show_session()
    # Створюємо резервацію, якщо її ще немає
    reservation = Reservation.objects.first() or sample_reservation()
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
        serializer = TicketListSerializer(tickets, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_ticket_detail(self):
        ticket = sample_ticket(row=2, seat=23)
        url = detail_url(ticket.id)

        response = self.client.get(url)

        ticket.refresh_from_db()

        serializer = TicketRetrieveSerializer(ticket)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_planetarium_dome(self):
        payload = {
            "name": "Sample Dome",
            "rows": 10,
            "seats": 23,
        }

        response = self.client.post(PLANETARIUMDOME_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTicketTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@test.com", password="testpassword", is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_ticket(self):
        payload = {
            "name": "Sample Dome",
            "rows": 10,
            "seats_in_row": 23,
        }

        response = self.client.post(PLANETARIUMDOME_URL, payload)

        self.assertIn('id', response.data)

        pland = PlanetariumDome.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(pland, key))

    def test_ticket_not_allowed(self):
        ticket = sample_ticket()

        url = detail_url(ticket.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
