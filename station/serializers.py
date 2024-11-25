from rest_framework import serializers
from .models import UltrasonicSensorData, ParkingLot

class UltrasonicSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UltrasonicSensorData
        fields = ['parking_lot', 'status', 'timestamp']

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ['name', 'location', 'total_spaces', 'available_spaces', 'moyenne_spaces']
