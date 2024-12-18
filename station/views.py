# parking/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ParkingLot, ParkingSpace, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
#from .forms import SignUpForm
from .forms import UserRegistrationForm, UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UltrasonicSensorData
from .serializers import UltrasonicSensorDataSerializer, ParkingLotSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required, login_required  
from django.core.exceptions import PermissionDenied  
from django.contrib.auth.models import Group  
from django.utils.dateformat import format
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required  
def make_reservation(request, parking_id):  
    if not request.user.has_perm('station.can_reserve_spot'):  
        raise PermissionDenied  


@login_required
def parking_list(request):
    if request.user.groups.filter(name="Clients").exists():  # Vérifie si l'utilisateur est dans le groupe "Clients"
        parkings = ParkingLot.objects.all()  # Charge tous les parkings
        return render(request, 'station/parking_list_clients.html', {'parkings': parkings})

    elif request.user.has_perm('station.can_view_parking'):  # Vérifie si l'utilisateur a le droit "can_view_parking"
        parkings = UltrasonicSensorData.objects.all()
        uid = UltrasonicSensorData.objects.last()
    return render(request, 'station/parking_list1.html', {'parkings': parkings, 'uids': uid})
    
    raise PermissionDenied  # Autres utilisateurs non autorisés



#Ajout fait pour les dernière modifications à revoir
@login_required
def reserve_parking(request, parking_id):
    parking_lot = get_object_or_404(ParkingLot, id=parking_id)
    available_spaces = parking_lot.spaces.filter(is_occupied=False)

    if request.method == 'POST':
        num_spaces = int(request.POST.get('num_spaces', 1))  # Nombre de places demandées
        if available_spaces.count() >= num_spaces:
            for _ in range(num_spaces):
                space = available_spaces.first()
                start_time = timezone.now()
                end_time = start_time + timezone.timedelta(hours=1)
                Reservation.objects.create(
                    user=request.user,
                    parking_space=space,
                    start_time=start_time,
                    end_time=end_time,
                    status='active'
                )
                space.is_occupied = True
                space.save()
            
            parking_lot.available_spaces -= num_spaces
            parking_lot.save()
            return redirect('reservation_list')

        return render(request, 'station/no_space_available.html', {'error': 'Not enough spaces available'})
    
    return render(request, 'station/reserve_parking.html', {'parking_lot': parking_lot, 'available_spaces': available_spaces.count()})


#ajout de vue fait pour visualiser en temps réel
def parking_status(request, parking_id):
    parking_lot = get_object_or_404(ParkingLot, id=parking_id)
    available_spaces = parking_lot.spaces.filter(is_occupied=False).count()
    return JsonResponse({'available_spaces': available_spaces})

def get_last_sensor_data(request):
    last_sensor_data = UltrasonicSensorData.objects.last()
    
    if last_sensor_data:
        data = {
            'id': last_sensor_data.id,
            'status': last_sensor_data.status,
            'parking_lot': last_sensor_data.parking_lot.name,
            'occupied_spaces': last_sensor_data.parking_lot.total_spaces - last_sensor_data.parking_lot.available_spaces
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'No data available'}, status=404)


@login_required
def reservation_list(request):
    if request.user.is_superuser:
        # Si l'utilisateur est un superutilisateur, il peut voir toutes les réservations
        reservations = Reservation.objects.all()
    else:
        # Sinon, il ne voit que ses propres réservations
        reservations = Reservation.objects.filter(user=request.user)
    
    return render(request, 'station/reservation_list.html', {'reservations': reservations})


def home_view(request):
    return render(request, 'station/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Vérifiez ou récupérez le groupe "Clients"
                client_group, created = Group.objects.get_or_create(name='Clients')
                user.groups.add(client_group)
                
                # Connecter l'utilisateur automatiquement après inscription
                login(request, user)
                messages.success(request, 'Votre compte a été créé avec succès!')
                return redirect('home')  # Assurez-vous que 'home' est défini dans vos URL
            except Exception as e:
                print(f"Erreur lors de la création de l'utilisateur: {e}")  # Pour le débogage
                messages.error(request, 'Une erreur est survenue lors de la création du compte.')
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'station/signup.html', {'form': form})


def home(request):
     # Vérifiez si l'utilisateur est authentifié
    if request.user.is_authenticated:
        username = request.user.username  # Récupérez le nom d'utilisateur
    else:
        username = None  # Si l'utilisateur n'est pas connecté

    # Passez le nom d'utilisateur au template
    return render(request, 'station/home.html', {'username': username})


class IsMicrocontroleur(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.username == 'microcontroleur'


class UltrasonicSensorDataView(APIView):

    permission_classes = [IsMicrocontroleur]  # Utilisez la nouvelle permission

    def get(self, request, *args, **kwargs):
        data = UltrasonicSensorData.objects.all()
        serializer = UltrasonicSensorDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UltrasonicSensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def allowed_methods(self):
    """
    Return the list of allowed HTTP methods, uppercased.
    """
    self.http_method_names.append("get")
    return [method.upper() for method in self.http_method_names
            if hasattr(self, method)]


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
class ParkingLotStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        parking_lots = ParkingLot.objects.all()
        serializer = ParkingLotSerializer(parking_lots, many=True)
        return Response(serializer.data)

def graph_view(request):
    data = UltrasonicSensorData.objects.filter(parking_lot_id=1).values('timestamp', 'status')
    formatted_data = [
        {
            'timestamp': format(item['timestamp'], 'Y-m-d H:i:s'),  # Format lisible
            'status': item['status']
        }
        for item in data
    ]
    serialized_data = json.dumps(formatted_data, cls=DjangoJSONEncoder)
    return render(request, 'station/graph.html', {'data': serialized_data})


from rest_framework.permissions import BasePermission