from rest_framework import serializers
from .models import *


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
        many=True,
        read_only=True,
        slug_field="title",
    )


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowSerializer(many=True)


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = "__all__"


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