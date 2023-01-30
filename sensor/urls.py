from django.urls import path
from sensor import views

app_name = 'sensor'

urlpatterns = [
    path('api/v1/add-sensor/', views.SensorDataCreateView.as_view(), name='post-sensor-data'),
    path('api/v1/get-sensor/', views.SensorDataListView.as_view(), name='get-sensor-data'),
]
