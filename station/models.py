# parking/models.py
from django.db import models
from django.contrib.auth.models import User

class ParkingLot(models.Model):
    name = models.CharField(max_length=255)
    ail_park = models.CharField(max_length=50, choices=[('Est', 'Est'), ('Ouest', 'Ouest'), ('Nord', 'Nord'), ('Sud', 'Sud')], default='Est')
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    available_spaces = models.IntegerField()
    moyenne_spaces = models.FloatField(default=0.0)  # Nouveau champ pour stocker la moyenne

    def __str__(self):
        return self.name
    
    def update_available_spaces(self):
        self.available_spaces = self.capacity - self.spaces.filter(is_occupied=True).count()
        self.save()

class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='spaces')
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'Space {self.id} in {self.parking_lot.name}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parking_lot.update_available_spaces()  # Met à jour les places disponibles après chaque réservation

    @staticmethod
    def get_default_parking_lot():
        # Retourne un ParkingLot par défaut (ajustez selon vos besoins)
        return ParkingLot.objects.first().id
    

class UltrasonicSensorData(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='ultrasonic_data')  # Lier au parking
    distance = models.FloatField()  # Distance mesurée par le capteur
    timestamp = models.DateTimeField(auto_now_add=True)  # Date de la mesure

    def __str__(self):
        return f'Distance: {self.distance} cm at {self.timestamp}'
