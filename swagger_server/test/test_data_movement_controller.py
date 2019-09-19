# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.req_body import ReqBody  # noqa: E501
from swagger_server.models.start_dm import StartDM  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDataMovementController(BaseTestCase):
    """DataMovementController integration test stubs"""

    def test_finish_movement(self):
        """Test case for finish_movement

        
        """
        response = self.client.open(
            '/finish_movement/',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_init_movement(self):
        """Test case for init_movement

        Initialize data movement for destination using transformation
        """
        body = ReqBody()
        response = self.client.open(
            '/init_movement/',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_movement(self):
        """Test case for start_movement

        Communication between DMEs. Signals the other DME to prepare for movement
        """
        body = StartDM()
        response = self.client.open(
            '/start_movement/',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
