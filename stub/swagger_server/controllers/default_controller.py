import connexion
import six

from swagger_server.models.accuracy import Accuracy  # noqa: E501
from swagger_server.models.humid_temp_data import HumidTempData  # noqa: E501
from swagger_server.models.sensor import Sensor  # noqa: E501
from swagger_server.models.water_plant import WaterPlant  # noqa: E501
from swagger_server import util


def controller_calculate_forecast_actual():  # noqa: E501
    """Compare forecast data and actual data from  https://data.tmd.go.th/api/Weather3Hours/ for the past 3 days and calculate accuracy.

     # noqa: E501


    :rtype: Accuracy[Sensor]
    """
    return 'do some magic!'


def controller_calculate_mape_sensors():  # noqa: E501
    """Compare forecast data from https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/ and sensors data for the past 3 days and calculate accuracy.

     # noqa: E501


    :rtype: Accuracy
    """
    return 'do some magic!'


def controller_get_actual3hrs_data():  # noqa: E501
    """Return actual data collected from TMD for the past 3 days

     # noqa: E501


    :rtype: List[HumidTempData]
    """
    return 'do some magic!'


def controller_get_forecast1hr_data():  # noqa: E501
    """Return forecast data collected from TMD for the past 3 days

     # noqa: E501


    :rtype: List[HumidTempData]
    """
    return 'do some magic!'


def controller_get_kidbright_sensors_data_hourly(duration):  # noqa: E501
    """Returns a list of sensor data in each hour of the past {duration} day.

     # noqa: E501

    :param duration: 
    :type duration: int

    :rtype: List[Sensor]
    """
    return 'do some magic!'


def controller_get_kidbright_sensors_data_hourly_by_date(_date):  # noqa: E501
    """Returns a list of sensor data in each hour in the specified date.

     # noqa: E501

    :param _date: 
    :type _date: str

    :rtype: List[Sensor]
    """
    return 'do some magic!'


def controller_get_latest_kidbright_sensors_data():  # noqa: E501
    """Returns the latest sensor data from kidbright.

     # noqa: E501


    :rtype: List[Sensor]
    """
    return 'do some magic!'


def controller_get_remind_water_my_plant():  # noqa: E501
    """Returns boolean indicating whether user should water their plant or not

     # noqa: E501


    :rtype: List[WaterPlant]
    """
    return 'do some magic!'
