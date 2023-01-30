import csv

from django.core.management.base import BaseCommand

from sensor.models import SensorData


class Command(BaseCommand):
    help = 'Import data from csv file'

    def handle(self, **options):
        with open('data.csv') as file:
            reader = csv.reader(file)
            next(reader)  # skip header

            for row in reader:
                sd = SensorData.objects.create(serial=row[0], application=row[1], time=row[2], type=row[3],
                                              device=row[4], v0=row[5], v18=row[23])
                sd.save()
                print("Successfully created SensorData object to database ", sd)
