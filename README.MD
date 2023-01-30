# Python backend assignment
    Project based on Python 3.10, Django and  Django REST Framework

## API Endpoints
    - /api/v1/add-sensor/ --> Add sensor data endpoint
    - /api/v1/get-sensor/ --> Get sensor data endpoint

## BasicAuthentication used for both endpoints and require to create User in database and use:
    username and password in request 
    I used basicauth just to protect API endpoints as requested here:"Make sure the sensor data endpoint is secured in some way so not everyone on the web is able to push new sensor data"
    but we can also use token auth

## Setup

* Prerequisite
    * We assume that you have docker already configured on your machine. If not, please install docker engine first.
    * Visit https://docs.docker.com/engine/install/ and choose your platform.

### Run Project
    
You need a running container to do this so, follow these steps

```terminal
# build 
docker-compose build

# start database and web containers
docker-compose up

# create superuser
docker-compose exec web ./manage.py createsuperuser

# launch a web browser to the api
open http://localhost:8000

# login in Django Admin dashboard, here you can create/view/edit/delete SensorData records
http://localhost:8000/admin
```

## Run tests

```terminal commands in root of the project
# start containers
docker-compose up

# run tests

docker-compose exec web ./manage.py test
```

## CSV import (optional)
```terminal
# start containers
docker-compose up

# Import data from csv file and save to database
docker-compose exec web ./manage.py import_data
```


## Test with Postman

```terminal commands in root of the project
# start server
docker-compose up

# create user in database and remember username and password
docker-compose exec web ./manage.py createsuperuser
```

# Open Postman app 
# Choose POST method 
# Url for adding data http://localhost:8000/api/v1/add-sensor/
# In Authorization tab choose type Basic Auth and pass username and password of user you just created above
# In Body tab select raw checkbox and JSON format
# Paste this json
{
    "message":{
        "attributes": {
            "key": "value"
        }, 
        "data": "eydzZXJpYWwnOiAnMDAwMTAwMDAwMTAwJywgJ2FwcGxpY2F0aW9uJzogMTEsICdUaW1lJzogJzIwMjItMTEtMDhUMDQ6MDA6MDQuMzE3ODAxJywgJ1R5cGUnOiAneGtndycsICdkZXZpY2UnOiAnVGVzdERldmljZScsICd2MCc6IDEwMDAxMywgJ3YxJzogMC42OSwgJ3YyJzogMS4zMSwgJ3YzJzogMC4xOCwgJ3Y0JzogMCwgJ3Y1JzogMC44LCAndjYnOiAwLCAndjcnOiAyNjk2NSwgJ3Y4JzogMC4xLCAndjknOiA5Nzc1NzQ5NiwgJ3YxMCc6IDAsICd2MTEnOiAwLCAndjEyJzogMS44NCwgJ3YxMyc6IDAsICd2MTQnOiAwLjcsICd2MTUnOiAxMDAxMCwgJ3YxNic6IDEwMDAxMywgJ3YxNyc6IDI2OTY1LCAndjE4JzogMi43Mn0=", 
            "messageId": "2070443601311540", 
            "message_id": "2070443601311540", 
            "publishTime": "2021-02-26T19:13:55.749Z", 
            "publish_time": "2021-02-26T19:13:55.749Z"
        }, 
    "subscription": "projects/myproject/subscriptions/mysubscription"
}
# Hit Send button
# You should receive in body of response created sensor data from database

# To get data you should do the following

# Open Postman app 
# Choose GET method 
# Url for getting data http://localhost:8000/api/v1/get-sensor/
# In Authorization tab choose type Basic Auth and pass username and password of user you just created above
# Hit Send button
# You should recevie all created sensor data from database

    