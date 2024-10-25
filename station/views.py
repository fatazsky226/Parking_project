# parking/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ParkingLot, ParkingSpace, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UserRegistrationForm, UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UltrasonicSensorData
from .serializers import UltrasonicSensorDataSerializer



def parking_list(request):
    parkings = ParkingLot.objects.all()
    return render(request, 'station/parking_list.html', {'parkings': parkings})

@login_required
def reserve_parking(request, parking_id):
    parking_lot = get_object_or_404(ParkingLot, id=parking_id)
    available_space = parking_lot.spaces.filter(is_occupied=False).first()

    # Nouvelle validation des conflits de réservation
    start_time = timezone.now()
    end_time = start_time + timezone.timedelta(hours=1)
    overlapping_reservations = Reservation.objects.filter(
        parking_space=available_space,
        start_time__lt=end_time,  # Réservation dont la fin est après le début demandé
        end_time__gt=start_time    # Réservation dont le début est avant la fin demandée
    )

    if available_space and not overlapping_reservations.exists():
        # Créer une réservation si aucun conflit
        reservation = Reservation.objects.create(
            user=request.user,
            parking_space=available_space,
            start_time=start_time,
            end_time=end_time,
            status='active'
        )

        # Marquer l'espace comme occupé
        available_space.is_occupied = True
        available_space.save()

        # Réduire le nombre de places disponibles dans le parking
        parking_lot.available_spaces -= 1
        parking_lot.save()

        return redirect('reservation_list')
    
    # Si aucune place disponible ou conflit de réservation
    return render(request, 'station/no_space_available.html')


@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'station/reservation_list.html', {'reservations': reservations})

def home_view(request):
    return render(request, 'station/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après inscription
    else:
        form = UserRegistrationForm()
    return render(request, 'station/register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = UserCreationForm()
    return render(request, 'station/signup.html', {'form': form})



def home(request):
    return render(request, 'station/home.html')



class UltrasonicSensorDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UltrasonicSensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
