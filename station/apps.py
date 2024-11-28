from django.apps import AppConfig


class StationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'station'

class ParkingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'station'

    def ready(self):
        import station.signals  # Assurez-vous que le signal est connecté

class StationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'station'

    def ready(self):
        import station.signals  # Importez les signaux
