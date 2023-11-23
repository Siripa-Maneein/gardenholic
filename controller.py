import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME
import datetime

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
        cs.execute("SELECT ts, lat, lon, soil, humid, temp, light FROM gardener")
        result = [models.Sensor(value[0], value[1], value[2], value[3], value[4], value[5]) for value in cs.fetchall()]
    return result

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
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
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

# def get_tmb_accuracy():
#     """Compare forecast api and actual api at the same hour for the past 3 days."""
#     return "Something"

# def get_tmb_sensors_accuracy():
#     """Compare forecast api and sensors data collected at the same hour for the past 3 days."""
#     return "Something"


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


# def get_stations(basin_id):
#     with pool.connection() as conn, conn.cursor() as cs:
#         cs.execute("""
#             SELECT station_id, s.ename
#             FROM station s
#             INNER JOIN basin b ON s.basin_id=b.basin_id
#             WHERE b.basin_id=%s
#             """, [basin_id])
#         result = [models.StationShort(station_id, name) for station_id, name in cs.fetchall()]
#     return result


# def get_station_details(station_id):
#     return "Do something"

