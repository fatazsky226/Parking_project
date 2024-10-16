# parking/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import ParkingLot, ParkingSpace, Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UserRegistrationForm, UserCreationForm

def parking_list(request):
    parkings = ParkingLot.objects.all()
    return render(request, 'station/parking_list.html', {'parkings': parkings})

@login_required
def reserve_parking(request, parking_id):
    parking_lot = get_object_or_404(ParkingLot, id=parking_id)
    available_space = parking_lot.spaces.filter(is_occupied=False).first()

    if available_space:
        # Créer une réservation
        reservation = Reservation.objects.create(
            user=request.user,
            parking_space=available_space,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            status='active'
        )

        # Marquer l'espace comme occupé
        available_space.is_occupied = True
        available_space.save()

        # Réduire le nombre de places disponibles dans le parking
        parking_lot.available_spaces -= 1  # On décrémente le nombre de places disponibles
        parking_lot.save()

        return redirect('reservation_list')
    
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
            return redirect('station/parking_list.html')  # Remplacez 'login' par l'URL de redirection souhaitée après l'inscription
    else:
        form = UserRegistrationForm()
    return render(request, 'station/register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'station/signup.html', {'form': form})


def home(request):
    return render(request, 'station/home.html')