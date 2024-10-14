from django.contrib import admin
from .models import *


class TickerInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    inlines = (TickerInLine,)


admin.site.register(Ticket)
admin.site.register(PlanetariumDome)
admin.site.register(ShowSession)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
