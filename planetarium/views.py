from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from planetarium.models import *
from planetarium.permissions import IsAdminALLORIsAuthenticatedOReadOnly
from planetarium.serializers import *


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminALLORIsAuthenticatedOReadOnly]


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        planetariumdome = self.get_object()
        serializer = self.get_serializer(planetariumdome, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related()
    serializer_class = TicketSerializer

    @staticmethod
    def _params_to_ints(query_string):
        return [int(str_id) for str_id in query_string.split(",")]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketRetrieveSerializer
        return TicketSerializer

    def get_queryset(self):
        queryset = self.queryset

        reservation = self.request.query_params.get("reservation")

        if reservation:
            reservation_ids = self._params_to_ints(reservation)
            queryset = queryset.filter(reservation__id__in=reservation_ids)

        if self.action in ("list", "retrieve"):
            return queryset.select_related()

        return queryset


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        elif self.action == 'retrieve':
            return ShowSessionRetrieveSerializer

        return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.select_related()

        return queryset
