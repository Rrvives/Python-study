from django.urls import path
from .views import AddVehicleView, VehicleListView, UpdateVehiclePricesView, DeleteVehiclesView

urlpatterns = [
    path('vehicles/add/', AddVehicleView.as_view(), name='add-vehicle'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/update-prices/', UpdateVehiclePricesView.as_view(), name='update-vehicle-prices'),
    path('vehicles/delete-old/', DeleteVehiclesView.as_view(), name='delete-vehicles'),
]