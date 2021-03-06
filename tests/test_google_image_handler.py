# -*- coding: utf-8 -*-
"""
    robo.tests.test_handler_google_image
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for robo.handlers.google_image


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import requests
from mock import patch
from unittest import TestCase
from robo.robot import Robot
from robo.handlers.google_image import Client, GoogleImage


def dummy_response(m, filename=None):
    response = requests.Response()
    response.status_code = 200
    if filename is None:
        response._content = ''
    else:
        root_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(root_path, filename)
        with open(file_path, 'r') as f:
            data = f.read()
        response._content = data

    m.return_value = response


class NullAdapter(object):
    def __init__(self, signal):
        self.signal = signal
        self.responses = []

    def say(self, message, **kwargs):
        self.responses.append(message)
        return message


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['ROBO_GOOGLE_CSE_KEY'] = 'foo'
        os.environ['ROBO_GOOGLE_CSE_ID'] = 'bar'
        cls.client = Client()

    @patch('robo.handlers.google_image.requests.get')
    def test_generate_url(self, m):
        """ Client().generate() should generate google search url. """
        dummy_response(m, 'fixture.json')
        ret = self.client.generate('cat')
        self.assertTrue(ret.startswith('http'))

    @patch('robo.handlers.google_image.requests.get')
    def test_search_resource(self, m):
        """ Client().search_resource() should search from Google. """
        dummy_response(m, 'fixture.json')
        ret = self.client.search_resource('cat')
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue('link' in ret)


class TestGoogleImageHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger('robo')
        logger.level = logging.ERROR
        cls.robot = Robot('test', logger)

        os.environ['ROBO_GOOGLE_CSE_KEY'] = 'foo'
        os.environ['ROBO_GOOGLE_CSE_ID'] = 'bar'

        client = GoogleImage()
        client.signal = cls.robot.handler_signal
        method = cls.robot.parse_handler_methods(client)
        cls.robot.handlers.extend(method)

        adapter = NullAdapter(cls.robot.handler_signal)
        cls.robot.adapters['null'] = adapter

    @patch('robo.handlers.google_image.requests.get')
    def test_should_google_image(self, m):
        """ GoogleImage().get() should search google. """
        dummy_response(m, 'fixture.json')
        self.robot.handler_signal.send('test image cat')
        import sys
        if sys.version_info[0] == 2:
            self.assertRegexpMatches(self.robot.adapters['null'].responses[0],
                                     r'^(http|https)://*')
        else:
            self.assertRegex(self.robot.adapters['null'].responses[0],
                             r'^(http|https)://*')

        self.robot.adapters['null'].responses = []
