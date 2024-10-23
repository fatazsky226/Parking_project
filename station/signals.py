# parking/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Reservation, ParkingLot

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Reservation)
def update_parking_spaces(sender, instance, **kwargs):
    parking_lot = instance.parking_lot
    if instance.status == 'reserved':
        parking_lot.available_spaces -= 1
    elif instance.status == 'cancelled':
        parking_lot.available_spaces += 1
    parking_lot.save()
