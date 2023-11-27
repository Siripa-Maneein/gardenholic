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
        cs.execute("""
                    SELECT ts, lat, lon, soil, humid, temp, light 
                    FROM gardener""")
        result = [models.Sensor(value[0], value[1], value[2], value[3], value[4], value[5]) for value in cs.fetchall()]
    return result


def get_latest_soil_humid():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT ts, soil
                    FROM gardener
                    ORDER by ts DESC
                    LIMIT 1
                """)
        result = [models.CurrentSoil(value[0], value[1]) for value in cs.fetchall()]
    return result

def get_forecast_humid():
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT ts, humid
                    FROM forecast
                    WHERE humid >= 90 AND ts >= NOW() AND ts <= DATE_ADD(NOW(), INTERVAL 24 HOUR)
                    ORDER BY ts DESC
                """)
        result = [models.ForcastHumid(value[0], value[1]) for value in cs.fetchall()]
    return result

def get_remind_water_my_plant():
    soil = get_latest_soil_humid()
    humid = get_forecast_humid()
    water = False  
    
    if int(soil[0].soil) < 50:
        if len(humid) > 0:
            if int(humid[0].humid) >= 90:
                water = False
        water = True
    else:
        water = False
    
    result = models.WaterPlant(water)
    return result

    
# def get_basin_details(basin_id):
#     with pool.connection() as conn, conn.cursor() as cs:
#         cs.execute("""
#             SELECT basin_id, ename, area
#             FROM basin
#             WHERE basin_id=%s
#             """, [basin_id])
#         result = cs.fetchone()
#     if result:
#         basin_id, name, area = result
#         return models.BasinFull(basin_id, name, area)
#     else:
#         abort(404)

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
        start_date = datetime.now()
        end_date = start_date - timedelta(days=3)

        cs.execute("""SELECT MIN(ts) AS ts, ROUND(AVG(lat), 4) AS lat,
                      ROUND(AVG(lon), 4) AS lon, AVG(humid) AS humid, AVG(temp) AS temp
                      FROM forecast 
                      WHERE ts BETWEEN %s AND %s
                      GROUP BY TIMESTAMPDIFF(HOUR, %s, ts) DIV 3 
                      ORDER BY ts;""", (end_date, start_date, end_date))


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
    total_percentage_error_temp = 0
    total_percentage_error_humid = 0
    total_count = 0

    forecast_data = get_forecast_3hrs_data()
    actual_data = get_actual_data()

    for forecast_entry in forecast_data:
        closest_actual_entry = min(actual_data, key=lambda x: abs((forecast_entry.time - x.time).total_seconds()))

        timestamp_tolerance_seconds = 60 
        if abs((forecast_entry.time - closest_actual_entry.time).total_seconds()) <= timestamp_tolerance_seconds:
            # Calculate percentage error for temperature
            percentage_error_temp = ((forecast_entry.temperature - closest_actual_entry.temperature) / closest_actual_entry.temperature) * 100
            total_percentage_error_temp += abs(percentage_error_temp)

            # Calculate percentage error for humidity
            percentage_error_humid = ((forecast_entry.humidity - closest_actual_entry.humidity) / closest_actual_entry.humidity) * 100
            total_percentage_error_humid += abs(percentage_error_humid)

            total_count += 1

    if total_count > 0:
        average_percentage_error_temp = total_percentage_error_temp / total_count
        forecast_accuracy_temp = 100 - average_percentage_error_temp

        average_percentage_error_humid = total_percentage_error_humid / total_count
        forecast_accuracy_humid = 100 - average_percentage_error_humid

        result = models.Accuracy(round(forecast_accuracy_humid, 2), round(forecast_accuracy_temp, 2))
        return [result] 

    return None

    
def calculate_mape_sensors():
    total_percentage_error_temp = 0
    total_percentage_error_humid = 0
    total_count = 0

    forecast_data = get_forecast_data()
    actual_data = get_avg_kidbright_sensors_data()
    accumulated_results = []

    for forecast_entry in forecast_data:
        closest_actual_entry = min(actual_data, key=lambda x: abs((forecast_entry.time - x.time).total_seconds()))

        timestamp_tolerance_seconds = 60  
        if abs((forecast_entry.time - closest_actual_entry.time).total_seconds()) <= timestamp_tolerance_seconds:
            # Calculate percentage error for temperature
            percentage_error_temp = abs((forecast_entry.temperature - closest_actual_entry.temperature) / closest_actual_entry.temperature) * 100
            total_percentage_error_temp += percentage_error_temp

            # Calculate percentage error for humidity
            percentage_error_humid = abs((forecast_entry.humidity - closest_actual_entry.humidity) / closest_actual_entry.humidity) * 100
            total_percentage_error_humid += percentage_error_humid

            total_count += 1

    if total_count > 0:
        average_percentage_error_temp = total_percentage_error_temp / total_count
        accuracy_temp = 100 - average_percentage_error_temp

        average_percentage_error_humid = total_percentage_error_humid / total_count
        accuracy_humid = 100 - average_percentage_error_humid

        result = models.Accuracy(round(accuracy_humid, 2), round(accuracy_temp, 2))
        accumulated_results.append(result)

    if accumulated_results:
        return accumulated_results
    else:
        return None
    
def get_kidbright_sensors_data_hourly():
    """Show time, lat, lon, soil, humidity, temperature, light data from kidbright source in each hour."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT DATE_FORMAT(ts, '%Y-%m-%d %H:00:00') AS hour_group, 
                    AVG(lat) AS avg_lat,
                    AVG(lon) AS avg_lon, 
                    AVG(soil) AS avg_soil, 
                    AVG(humid) AS avg_humid, 
                    AVG(temp) AS avg_temp, 
                    AVG(light) AS avg_light 
                    FROM gardener 
                    GROUP BY hour_group
                    """)
        current_date = datetime.now().strftime('%Y-%m-%d')
        result = [models.Sensor(value[0], round(value[1], 2), round(value[2], 2), round(value[3], 2), round(value[4], 2), round(value[5], 2)) for value in cs.fetchall() if current_date in str(value[0])]
    return result

def get_kidbright_sensors_data_hourly_by_date(date):
    """Show time, lat, lon, soil, humidity, temperature, light data from kidbright source in each hour in a specific date."""
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
                    SELECT DATE_FORMAT(ts, '%Y-%m-%d %H:00:00') AS hour_group, 
                    AVG(lat) AS avg_lat,
                    AVG(lon) AS avg_lon, 
                    AVG(soil) AS avg_soil, 
                    AVG(humid) AS avg_humid, 
                    AVG(temp) AS avg_temp, 
                    AVG(light) AS avg_light 
                    FROM gardener 
                    GROUP BY hour_group
                    """)
        result = [models.Sensor(value[0], round(value[1], 2), round(value[2], 2), round(value[3], 2), round(value[4], 2), round(value[5], 2)) for value in cs.fetchall() if date in str(value[0])]
    return result