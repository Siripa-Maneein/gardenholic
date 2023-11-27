import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

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
    # result = models.WaterPlant(humid)
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

