# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Accuracy(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, humidity_accuracy_percentage: int=None, temperature_accuracy_percentage: int=None):  # noqa: E501
        """Accuracy - a model defined in Swagger

        :param humidity_accuracy_percentage: The humidity_accuracy_percentage of this Accuracy.  # noqa: E501
        :type humidity_accuracy_percentage: int
        :param temperature_accuracy_percentage: The temperature_accuracy_percentage of this Accuracy.  # noqa: E501
        :type temperature_accuracy_percentage: int
        """
        self.swagger_types = {
            'humidity_accuracy_percentage': int,
            'temperature_accuracy_percentage': int
        }

        self.attribute_map = {
            'humidity_accuracy_percentage': 'humidity_accuracy_percentage',
            'temperature_accuracy_percentage': 'temperature_accuracy_percentage'
        }
        self._humidity_accuracy_percentage = humidity_accuracy_percentage
        self._temperature_accuracy_percentage = temperature_accuracy_percentage

    @classmethod
    def from_dict(cls, dikt) -> 'Accuracy':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Accuracy of this Accuracy.  # noqa: E501
        :rtype: Accuracy
        """
        return util.deserialize_model(dikt, cls)

    @property
    def humidity_accuracy_percentage(self) -> int:
        """Gets the humidity_accuracy_percentage of this Accuracy.


        :return: The humidity_accuracy_percentage of this Accuracy.
        :rtype: int
        """
        return self._humidity_accuracy_percentage

    @humidity_accuracy_percentage.setter
    def humidity_accuracy_percentage(self, humidity_accuracy_percentage: int):
        """Sets the humidity_accuracy_percentage of this Accuracy.


        :param humidity_accuracy_percentage: The humidity_accuracy_percentage of this Accuracy.
        :type humidity_accuracy_percentage: int
        """

        self._humidity_accuracy_percentage = humidity_accuracy_percentage

    @property
    def temperature_accuracy_percentage(self) -> int:
        """Gets the temperature_accuracy_percentage of this Accuracy.


        :return: The temperature_accuracy_percentage of this Accuracy.
        :rtype: int
        """
        return self._temperature_accuracy_percentage

    @temperature_accuracy_percentage.setter
    def temperature_accuracy_percentage(self, temperature_accuracy_percentage: int):
        """Sets the temperature_accuracy_percentage of this Accuracy.


        :param temperature_accuracy_percentage: The temperature_accuracy_percentage of this Accuracy.
        :type temperature_accuracy_percentage: int
        """

        self._temperature_accuracy_percentage = temperature_accuracy_percentage