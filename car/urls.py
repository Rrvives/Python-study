from django.urls import path
from . import views

urlpatterns = [
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('update_prices/', views.update_vehicle_prices, name='update_prices'),
    path('delete_vehicles/', views.delete_vehicles, name='delete_vehicles'),
]