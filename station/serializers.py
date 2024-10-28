from rest_framework import serializers
from .models import UltrasonicSensorData

class UltrasonicSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UltrasonicSensorData
        fields = ['parking_lot', 'distance', 'timestamp']


