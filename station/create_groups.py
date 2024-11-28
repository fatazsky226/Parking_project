from django.core.management.base import BaseCommand  
from django.contrib.auth.models import Group, Permission  
from django.contrib.contenttypes.models import ContentType  
from station.models import Profile  # et vos autres modèles  

class Command(BaseCommand):  
    help = 'Crée les groupes et permissions par défaut'  

    def handle(self, *args, **options):  
        # Création des groupes  
        admin_group, _ = Group.objects.get_or_create(name='Administrateurs')  
        client_group, _ = Group.objects.get_or_create(name='Clients')  
        staff_group, _ = Group.objects.get_or_create(name='Personnel')  

        # Obtenir le type de contenu pour vos modèles  
        profile_content_type = ContentType.objects.get_for_model(Profile)  

        # Créer des permissions personnalisées  
        view_all_profiles = Permission.objects.create(  
            codename='view_all_profiles',  
            name='Peut voir tous les profils',  
            content_type=profile_content_type,  
        )  
        manage_reservations = Permission.objects.create(  
            codename='manage_reservations',  
            name='Peut gérer les réservations',  
            content_type=profile_content_type,  
        )  

        # Attribuer les permissions aux groupes  
        admin_group.permissions.add(view_all_profiles, manage_reservations)  
        staff_group.permissions.add(view_all_profiles)