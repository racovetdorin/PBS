from django.db import models
from django.core.validators import MinValueValidator


class SensorData(models.Model):
    """Sensor data received from Google Cloud Pub/Sub"""
    serial = models.CharField(verbose_name='serial', max_length=150, blank=False)
    application = models.PositiveIntegerField(verbose_name='application',  blank=False)
    time = models.DateTimeField(verbose_name='Time',  blank=False)
    type = models.CharField(verbose_name='Type', max_length=150,  blank=False)
    device = models.CharField(verbose_name='device', max_length=150, blank=False)
    v0 = models.PositiveIntegerField(verbose_name='Origin sensor Id', blank=False)
    v18 = models.FloatField(verbose_name='dwell time', validators=[MinValueValidator(0.0)], blank=False)

    class Meta:
        db_table = 'sensor_data'
        ordering = ['time']
