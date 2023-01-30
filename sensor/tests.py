import base64
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from .models import SensorData


class SensorDataAPITestCase(APITestCase):
    def setUp(self):
        self.python_dict = {
            "serial": "000100000100",
            "application": 11,
            "Time": "2022-11-08T04:00:04.317801",
            "Type": "xkgw",
            "device": "TestDevice",
            "v0": 100013,
            "v1": 0.69,
            "v2": 1.31,
            "v3": 0.18,
            "v4": 0,
            "v5": 0.8,
            "v6": 0,
            "v7": 26965,
            "v8": 0.1,
            "v9": 97757496,
            "v10": 0,
            "v11": 0,
            "v12": 1.84,
            "v13": 0,
            "v14": 0.7,
            "v15": 10010,
            "v16": 100013,
            "v17": 26965,
            "v18": 2.72
        }
        self.encoded_dict = str(self.python_dict).encode('utf-8')
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        # login user in order to can make requests
        self.client.force_authenticate(user=self.user)
        self.message = {
            "message": {
                "attributes": {
                    "key": "value"
                },
                "data": base64.b64encode(self.encoded_dict),
                "messageId": "2070443601311540",
                "message_id": "2070443601311540",
                "publishTime": "2021-02-26T19:13:55.749Z",
                "publish_time": "2021-02-26T19:13:55.749Z"
            },
            "subscription": "projects/myproject/subscriptions/mysubscription"
        }

    def test_api_authentication_successfully(self):
        url = reverse('sensor:post-sensor-data')
        response = self.client.post(url, self.message, format='json')
        self.assertEqual(response.status_code, 201)

    def test_api_authentication_unsuccessfully(self):
        url = reverse('sensor:post-sensor-data')
        self.client.logout()
        response = self.client.post(url, self.message, format='json')
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 401)

    def test_create_sensordata_successfully(self):
        url = reverse('sensor:post-sensor-data')
        response = self.client.post(url, self.message, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SensorData.objects.all().count(), 1)

    def test_create_sensordata_unsuccessfully(self):
        url = reverse('sensor:post-sensor-data')
        message = self.message['data'] = "fake data here"
        response = self.client.post(url, message, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SensorData.objects.all().count(), 0)

    def test_filter_query_params(self):
        """Test Get SensorData query params filtering"""
        url_post = reverse('sensor:post-sensor-data')
        self.client.post(url_post, self.message, format='json')

        from_date = '2022-11-07'
        to_date = '2022-11-10'
        sensor_id = 100013

        url_get = reverse('sensor:get-sensor-data') + f'?from_date={from_date}&to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.status_code, 200)

        from_date = '2022-11-09'

        url_get = reverse('sensor:get-sensor-data') + f'?from_date={from_date}&to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(response.status_code, 200)

        sensor_id = 'sfadsfde123'

        url_get = reverse('sensor:get-sensor-data') + f'?from_date={from_date}&to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.json(), {"error": "Incorrect sensor_id parameter format, should be integer"})
        self.assertEqual(response.status_code, 400)

        from_date = '07-11-2022'
        sensor_id = 100014

        url_get = reverse('sensor:get-sensor-data') + f'?from_date={from_date}&to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.json(), {"error": "Incorrect from_date or to_date parameter format, should be YYYY-MM-DD"})
        self.assertEqual(response.status_code, 400)

        to_date = '2022-11-10H'

        url_get = reverse('sensor:get-sensor-data') + f'?to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.json(), {"error": "Incorrect to_date parameter format, should be YYYY-MM-DD"})
        self.assertEqual(response.status_code, 400)

        to_date = '2022-11-04'
        from_date = '2022-11-07'

        url_get = reverse('sensor:get-sensor-data') + f'?from_date={from_date}&to_date={to_date}&sensor_id={sensor_id}'
        response = self.client.get(url_get, format='json')

        self.assertEqual(response.json(), {"error": "from_date parameter can't be greater than to_date"})
        self.assertEqual(response.status_code, 400)
