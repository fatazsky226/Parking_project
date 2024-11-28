from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import ParkingLot, ParkingSpace, Reservation, Profile, CustomUser

# Désenregistrer User uniquement s'il est déjà enregistré
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'contact_number')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')  # Ces champs sont sur CustomUser, pas sur Profile
    ordering = ('username',)

# Enregistrer Profile dans l'admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'contact_number')

admin.site.register(User, CustomUserAdmin)

# Enregistrement des autres modèles
@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_spaces', 'location', 'available_spaces']
    search_fields = ('name', 'location')

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking_lot', 'is_occupied')
    list_filter = ('is_occupied',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parking_space', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('user__username', 'parking_space__parking_lot__name')
