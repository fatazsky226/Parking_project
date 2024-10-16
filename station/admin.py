# parking/admin.py

from django.contrib import admin
from .models import ParkingLot, ParkingSpace, Reservation, Profile

@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'available_spaces', 'ail_park')  # Affiche ces champs dans l'admin
    search_fields = ('name', 'location')  # Permet de rechercher par nom ou emplacement

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking_lot', 'is_occupied')  # Affiche l'ID, le parking et le statut d'occupation
    list_filter = ('is_occupied',)  # Permet de filtrer par espace occupé

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parking_space', 'start_time', 'end_time', 'status')  # Affiche ces champs
    list_filter = ('status', 'start_time')  # Permet de filtrer par statut et date de début
    search_fields = ('user__username', 'parking_space__parking_lot__name')  # Recherche par utilisateur et parking

admin.site.register(Profile)
