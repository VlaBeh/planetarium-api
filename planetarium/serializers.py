from rest_framework import serializers
from .models import *


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "created_at")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = "__all__"


class AstronomyShowListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="title",
    )


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title",
    )

    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowSerializer()


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = "__all__"


class PlanetariumDomeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = ("id", "image")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class TicketListSerializer(serializers.ModelSerializer):
    show_info = serializers.CharField(source="show_session.astronomy_show.title", read_only=True)
    show_seat = serializers.IntegerField(source="ticket.seat", read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketRetrieveSerializer(TicketSerializer):
    show_session = ShowSessionRetrieveSerializer(many=False, read_only=True)

    def get_show_session(self, obj):
        return {
            'id': obj.show_session.id,
            'astronomy_show': obj.show_session.astronomy_show.title,
            'session_date': obj.show_session.show_time.strftime('%Y-%m-%d'),
            'planetarium_dome': obj.show_session.planetarium_dome.id,
        }
