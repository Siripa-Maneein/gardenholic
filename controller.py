import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from datetime import datetime, timedelta

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)

def get_kidbright_sensors_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""SELECT ts, lat, lon, soil, humid, temp, light 
                   FROM gardener""")
        result = [models.Sensor(value[0], value[1], value[2], value[3], value[4], value[5]) for value in cs.fetchall()]
    return result

def get_avg_kidbright_sensors_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""SELECT lat, lon, DATE_FORMAT(ts, '%%Y-%%m-%%d %%H:00:00') AS hour,
                   AVG(temp) AS temp, AVG(humid) AS humid
                   FROM gardener 
                   WHERE ts >= %s
                   GROUP BY lat, lon, hour ORDER BY hour""",
                   ((datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:00:00'),))
        result = [models.Forecast(datetime.strptime(value[2], '%Y-%m-%d %H:00:00'), value[0], value[1], value[3], value[4]) for value in cs.fetchall()]
    return result




def get_forecast_3hrs_data():
    with pool.connection() as conn, conn.cursor() as cs:
        # Specify the start date
        start_date = datetime.strptime('2023-11-22 10:00:00', '%Y-%m-%d %H:%M:%S')

        # Calculate the end date (start date + 3 days)
        end_date = start_date + timedelta(days=3)

        cs.execute("""SELECT MIN(ts) AS ts, ROUND(AVG(lat), 4) AS lat,
                      ROUND(AVG(lon), 4) AS lon, AVG(humid) AS humid, AVG(temp) AS temp
                      FROM forecast 
                      WHERE ts BETWEEN %s AND %s
                      GROUP BY TIMESTAMPDIFF(HOUR, %s, ts) DIV 3 
                      ORDER BY ts;""", (start_date, end_date, start_date))

        result = [models.Forecast(value[0], value[1], value[2], value[3], value[4]) for value in cs.fetchall()]
    return result





def get_actual_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("SELECT ts, lat, lon, humid, temp FROM actual "
                   "WHERE ts >= %s", (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:00:00'))
        result = [models.Forecast(value[0], value[1], value[2], value[3], value[4]) for value in cs.fetchall()]
    return result

def get_forecast_data():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("SELECT ts, lat, lon, humid, temp FROM forecast "
                   "WHERE ts >= %s", (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:00:00'))
        result = [models.Forecast(value[0], value[1], value[2], value[3], value[4]) for value in cs.fetchall()]
    return result

def calculate_forecast_actual():
    total_error_temp = 0
    total_error_humid = 0
    total_count = 0
    forecast_data = get_forecast_3hrs_data()
    actual_data = get_actual_data()
    accumulated_results = []

    for forecast_entry in forecast_data:
        closest_actual_entry = min(actual_data, key=lambda x: abs((forecast_entry.time - x.time).total_seconds()))

        # Check if the entries correspond to the same timestamp within a tolerance
        timestamp_tolerance_seconds = 60  # Adjust as needed
        if abs((forecast_entry.time - closest_actual_entry.time).total_seconds()) <= timestamp_tolerance_seconds:
            # Calculate MAPE for temperature
            error_temp = abs((forecast_entry.temperature - closest_actual_entry.temperature) / closest_actual_entry.temperature) * 100
            total_error_temp += error_temp

            # Calculate MAPE for humidity
            error_humid = abs((forecast_entry.humidity - closest_actual_entry.humidity) / closest_actual_entry.humidity) * 100
            total_error_humid += error_humid

            total_count += 1

            # Calculate accuracy and append to accumulated_results
            if total_count > 0:
                average_error_temp = total_error_temp / total_count
                accuracy_temp = 100 - average_error_temp

                average_error_humid = total_error_humid / total_count
                accuracy_humid = 100 - average_error_humid
                result = models.Accuracy(round(accuracy_humid, 2), round(accuracy_temp, 2))
                accumulated_results.append(result)

    if accumulated_results:
        return accumulated_results
    else:
        return None  # Handle the case where there is no corresponding actual data for any forecast entry
def calculate_mape_sensors():
    total_error_temp = 0
    total_error_humid = 0
    total_count = 0
    forecast_data = get_forecast_data()
    actual_data = get_avg_kidbright_sensors_data()
    accumulated_results = []

    for forecast_entry in forecast_data:
        closest_actual_entry = min(actual_data, key=lambda x: abs((forecast_entry.time - x.time).total_seconds()))

        # Check if the entries correspond to the same timestamp within a tolerance
        timestamp_tolerance_seconds = 60  # Adjust as needed
        if abs((forecast_entry.time - closest_actual_entry.time).total_seconds()) <= timestamp_tolerance_seconds:
            # Calculate MAPE for temperature
            error_temp = abs((forecast_entry.temperature - closest_actual_entry.temperature) / closest_actual_entry.temperature) * 100
            total_error_temp += error_temp

            # Calculate MAPE for humidity
            error_humid = abs((forecast_entry.humidity - closest_actual_entry.humidity) / closest_actual_entry.humidity) * 100
            total_error_humid += error_humid

            total_count += 1

            # Calculate accuracy and append to accumulated_results
            if total_count > 0:
                average_error_temp = total_error_temp / total_count
                accuracy_temp = 100 - average_error_temp

                average_error_humid = total_error_humid / total_count
                accuracy_humid = 100 - average_error_humid
                result = models.Accuracy(round(accuracy_humid, 2), round(accuracy_temp, 2))
                accumulated_results.append(result)

    if accumulated_results:
        return accumulated_results
    else:
        return None 