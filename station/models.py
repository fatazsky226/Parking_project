# station/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class ParkingLot(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    total_spaces = models.IntegerField()
    available_spaces = models.IntegerField(default=0)  # Places disponibles calculées
    moyenne_spaces = models.FloatField(default=0.0)  # Champ pour stocker la moyenne des distances

    def __str__(self):
        return self.name

    def update_available_spaces(self):
        self.available_spaces = self.total_spaces - self.spaces.filter(is_occupied=True).count()
        self.save()

    def update_average_distance(self):
        data_points = self.ultrasonic_data.all()
        if data_points.exists():
            self.moyenne_spaces = sum(d.status == "Occupé" for d in data_points) / len(data_points)
        self.save()
    
    class Meta:  
        permissions = [  
            ("can_view_parking", "Peut voir le parking"),  
            ("can_manage_parking", "Peut gérer le parking"),  
            ("can_reserve_spot", "Peut réserver une place"),  
        ] 

class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='spaces')
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'Space {self.id} in {self.parking_lot.name}'
    
from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    
    
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parking_space.parking_lot.update_available_spaces()

    @staticmethod
    def get_default_parking_lot():
        # Retourne un ParkingLot par défaut (ajustez selon vos besoins)
        return ParkingLot.objects.first().id
    
    class Meta:  
        permissions = [  
            ("can_view_all_reservations", "Peut voir toutes les réservations"),  
            ("can_manage_reservations", "Peut gérer les réservations"),  
        ]
    

class UltrasonicSensorData(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='ultrasonic_data')
    status = models.CharField(max_length=100)  # "Occupé" ou "Libre"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.status} at {self.timestamp}'

class AverageDistance(models.Model):
    parking_lot = models.OneToOneField('ParkingLot', on_delete=models.CASCADE, related_name='average_distance')
    average_distance = models.FloatField(default=0.0)  # Stocke la moyenne calculée
    last_updated = models.DateTimeField(default=timezone.now)  # Horodatage de la dernière mise à jour

    def __str__(self):
        return f'Average distance for {self.parking_lot.name}: {self.average_distance} cm'
