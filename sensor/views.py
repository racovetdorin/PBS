import base64
from datetime import datetime
import jsonschema
from jsonschema import validate
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer
from .utils import SENSOR_DATA_SCHEMA


class SensorDataCreateView(CreateAPIView):
    """
    Create SensorData API view that handle only POST method and create SensorData database records
    This view use BasicAuthentication (username, password)
    Requests are available only for existing database users
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SensorDataSerializer

    def post(self, request):
        try:
            # validate incoming json using validation schema
            validate(instance=request.data, schema=SENSOR_DATA_SCHEMA)
        except jsonschema.exceptions.ValidationError as err:
            return Response({'error': err.message}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # decode json data
            decoded_data = eval(base64.b64decode(request.data['message']['data']))
            data = {
                'serial': decoded_data['serial'],
                'application': decoded_data['application'],
                'time': decoded_data['Time'],
                'type': decoded_data['Type'],
                'device': decoded_data['device'],
                'v0': decoded_data['v0'],
                'v18': decoded_data['v18'],
            }
        except KeyError:
            return Response({'error': 'json does not contain the necessary data.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SensorDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SensorDataListView(ListAPIView):
    """
    List SensorData API view that handle only GET method
    This view use BasicAuthentication (username, password)
    Requests are available only for existing database users
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SensorDataSerializer

    def get_queryset(self):
        """
        Override get_queryset method and check 3 query params:
            sensor_id -> origin sensor id which works as an identifier (v0 field)
            from_date -> date min: 2022-11-07 (time field)
            to_date -> date max: 2022-11-08 (time field)
        """
        queryset = SensorData.objects.all()
        from_date = self.request.query_params.get('from_date')
        to_date = self.request.query_params.get('to_date')
        sensor_id = self.request.query_params.get('sensor_id')
        if sensor_id is not None:
            if not sensor_id.isnumeric():
                raise ValidationError({"error": "Incorrect sensor_id parameter format, should be integer"})
            queryset = queryset.filter(v0=sensor_id)
        if from_date is not None and to_date is not None:
            try:
                from_date_object = datetime.strptime(from_date, '%Y-%m-%d')
                to_date_object = datetime.strptime(to_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                if from_date_object > to_date_object:
                    raise ValidationError({"error": "from_date parameter can't be greater than to_date"})
                queryset = queryset.filter(time__gte=from_date_object, time__lte=to_date_object)
                return queryset
            except ValueError:
                raise ValidationError({"error": "Incorrect from_date or to_date parameter format, should be YYYY-MM-DD"})
        if from_date is not None:
            try:
                datetime.strptime(from_date, '%Y-%m-%d')
                queryset = queryset.filter(time__gte=from_date)
            except ValueError:
                raise ValidationError({"error": "Incorrect from_date parameter format, should be YYYY-MM-DD"})
        if to_date is not None:
            try:
                to_date_object = datetime.strptime(to_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
                queryset = queryset.filter(time__lte=to_date_object)
            except ValueError:
                raise ValidationError({"error": "Incorrect to_date parameter format, should be YYYY-MM-DD"})
        return queryset
