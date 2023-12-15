# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.accuracy import Accuracy  # noqa: E501
from swagger_server.models.humid_temp_data import HumidTempData  # noqa: E501
from swagger_server.models.sensor import Sensor  # noqa: E501
from swagger_server.models.water_plant import WaterPlant  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_controller_calculate_forecast_actual(self):
        """Test case for controller_calculate_forecast_actual

        Compare forecast data and actual data from  https://data.tmd.go.th/api/Weather3Hours/ for the past 3 days and calculate accuracy.
        """
        response = self.client.open(
            '/tmd_accuracy',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_calculate_mape_sensors(self):
        """Test case for controller_calculate_mape_sensors

        Compare forecast data from https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/ and sensors data for the past 3 days and calculate accuracy.
        """
        response = self.client.open(
            '/tmd_accuracy/sensors',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_actual3hrs_data(self):
        """Test case for controller_get_actual3hrs_data

        Return actual data collected from TMD for the past 3 days
        """
        response = self.client.open(
            '/actual_data',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_forecast1hr_data(self):
        """Test case for controller_get_forecast1hr_data

        Return forecast data collected from TMD for the past 3 days
        """
        response = self.client.open(
            '/forecast_data',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_sensors_data_hourly(self):
        """Test case for controller_get_kidbright_sensors_data_hourly

        Returns a list of sensor data in each hour of the past {duration} day.
        """
        response = self.client.open(
            '/sensors_hourly/{duration}'.format(duration=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_kidbright_sensors_data_hourly_by_date(self):
        """Test case for controller_get_kidbright_sensors_data_hourly_by_date

        Returns a list of sensor data in each hour in the specified date.
        """
        response = self.client.open(
            '/sensors_hourly_by_date/{date}'.format(_date='_date_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_latest_kidbright_sensors_data(self):
        """Test case for controller_get_latest_kidbright_sensors_data

        Returns the latest sensor data from kidbright.
        """
        response = self.client.open(
            '/latest_sensor',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_controller_get_remind_water_my_plant(self):
        """Test case for controller_get_remind_water_my_plant

        Returns boolean indicating whether user should water their plant or not
        """
        response = self.client.open(
            '/should_I_water_my_plant',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
