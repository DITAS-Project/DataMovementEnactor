# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.database_inner_columns import DatabaseInnerColumns  # noqa: F401,E501
from swagger_server import util


class DatabaseInnerTables(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, table_id: str=None, columns: List[DatabaseInnerColumns]=None):  # noqa: E501
        """DatabaseInnerTables - a model defined in Swagger

        :param table_id: The table_id of this DatabaseInnerTables.  # noqa: E501
        :type table_id: str
        :param columns: The columns of this DatabaseInnerTables.  # noqa: E501
        :type columns: List[DatabaseInnerColumns]
        """
        self.swagger_types = {
            'table_id': str,
            'columns': List[DatabaseInnerColumns]
        }

        self.attribute_map = {
            'table_id': 'table_id',
            'columns': 'columns'
        }
        self._table_id = table_id
        self._columns = columns

    @classmethod
    def from_dict(cls, dikt) -> 'DatabaseInnerTables':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The database_inner_tables of this DatabaseInnerTables.  # noqa: E501
        :rtype: DatabaseInnerTables
        """
        return util.deserialize_model(dikt, cls)

    @property
    def table_id(self) -> str:
        """Gets the table_id of this DatabaseInnerTables.


        :return: The table_id of this DatabaseInnerTables.
        :rtype: str
        """
        return self._table_id

    @table_id.setter
    def table_id(self, table_id: str):
        """Sets the table_id of this DatabaseInnerTables.


        :param table_id: The table_id of this DatabaseInnerTables.
        :type table_id: str
        """

        self._table_id = table_id

    @property
    def columns(self) -> List[DatabaseInnerColumns]:
        """Gets the columns of this DatabaseInnerTables.


        :return: The columns of this DatabaseInnerTables.
        :rtype: List[DatabaseInnerColumns]
        """
        return self._columns

    @columns.setter
    def columns(self, columns: List[DatabaseInnerColumns]):
        """Sets the columns of this DatabaseInnerTables.


        :param columns: The columns of this DatabaseInnerTables.
        :type columns: List[DatabaseInnerColumns]
        """

        self._columns = columns
