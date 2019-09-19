# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.database_inner import DatabaseInner  # noqa: F401,E501
from swagger_server import util


class Database(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self):  # noqa: E501
        """Database - a model defined in Swagger

        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Database':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The database of this Database.  # noqa: E501
        :rtype: Database
        """
        return util.deserialize_model(dikt, cls)
