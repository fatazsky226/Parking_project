
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home_view, signup, UltrasonicSensorDataView, ParkingLotStatusView, parking_list, graph_view


urlpatterns = [
    path('parking/', views.parking_list, name='parking_list'),
    path('', views.home, name='station-home'),  # Assurez-vous d'avoir une vue définie
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('api/last_sensor_data/', views.get_last_sensor_data, name='get_last_sensor_data'),
    path('signup/', views.signup, name='signup'),  # URL d'inscription
    path('login/', auth_views.LoginView.as_view(template_name='station/login.html', next_page='/station/parking/'), name='login'),  # URL de connexion
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL de déconnexion
    path('logout/', auth_views.LogoutView.as_view(next_page='/station'), name='logout'),
    path('', views.home, name='home'),  # URL de la page d'accueil
    path('api/ultrasonic/', UltrasonicSensorDataView.as_view(), name='ultrasonic_data'),
    path('api/parking_status/', ParkingLotStatusView.as_view(), name='get_parking_status'),
    path('graph/', views.graph_view, name='graph'),
]
