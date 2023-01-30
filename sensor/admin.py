from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilter, NumericRangeFilter

from .models import SensorData


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial', 'application', 'time', 'type', 'device', 'v0', 'v18')
    search_fields = ('v0',)
    list_filter = (
        ('time', DateTimeRangeFilter),
        ('v0', NumericRangeFilter),
        ('v18', NumericRangeFilter)
    )
