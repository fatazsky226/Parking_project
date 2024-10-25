
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home_view, register, signup, UltrasonicSensorDataView


urlpatterns = [
    path('parking/', views.parking_list, name='parking_list'),
    path('', views.home, name='station-home'),  # Assurez-vous d'avoir une vue définie
    path('reserve/<int:parking_id>/', views.reserve_parking, name='reserve_parking'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('acceuil/', home_view, name='home'),
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='station/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ultrasonic/', UltrasonicSensorDataView.as_view(), name='ultrasonic_data'),
]
