GardenHolic API Server
===============

API

1. /sensors_hourly <br>
Show time, lat, lon, soil, humidity, temperature, light data from kidbright source in each hour
    Response example:
    ```
    [
    {
        "humidity": 57,
        "lat": 13.5795,
        "light": 165.523,
        "lon": 100.593,
        "soil": 0,
        "temperature": 27.25,
        "time": "2023-11-22T10:00:00Z"
    },
    {
        "humidity": 57,
        "lat": 13.5795,
        "light": 165.523,
        "lon": 100.593,
        "soil": 0,
        "temperature": 27.25,
        "time": "2023-11-22T11:00:00Z"
    }, ...
    ]
    ```

2. /sensors_hourly/{date} <br>
Show time, lat, lon, soil, humidity, temperature, light data from kidbright source in each hour in a specific date

    /sensors_hourly/2023-11-22

    Response example:
    ```
    [
    {
        "humidity": 57,
        "lat": 13.5795,
        "light": 165.523,
        "lon": 100.593,
        "soil": 0,
        "temperature": 27.25,
        "time": "2023-11-22T00:00:00Z"
    }, ...,
    {
        "humidity": 57,
        "lat": 13.5795,
        "light": 165.523,
        "lon": 100.593,
        "soil": 0,
        "temperature": 27.25,
        "time": "2023-11-22T23:00:00Z"
    }
    ]
    ```

4. /tmb_accuracy <br>
Compare forecast api and actual api at the same hour for the past 3 days

    ***Noted that the forecast data need to be grouped into 3-hours interval first.

    Use MAPE forecast accuracy (Mean Absolute Percentage Error) to compare
    1. Calculate the %error between values at the same hour of the past 3 days
    ```
    %error = diff(forecast - actual) / actual * 100
    ```

    2. Find Average of %Error
    ```
    %AverageError = sum(%error) / number_of_rows
    ```

    3. Find %Accuracy
    ```
    %Accuracy = 100 - %AverageError
    ```
    For more information about MAPE visit: https://abcsupplychain.com/forecast-accuracy/#:~:text=The%20forecast%20accuracy%20formula%20is,errors%20by%20the%20total%20demand.


    Response example:
    ```
    {
        "humidity_accuracy_percentage": 92,
        "temperature_accuracy_percentage": 90,
    }
    ```
    
5. /tmb_accuracy/sensors <br>
Compare forecast api and sensors data collected at the same hour for the past 3 days

    ***Noted that the sensors data need to be grouped into 1-hour interval first.

    Silimar to 4 but change the compared data to the sensors that we collect ourselves

    Response example:
    ```
    {
        "humidity_accuracy_percentage": 90,
        "temperature_accuracy_percentage": 89,
    }
    ```