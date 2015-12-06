# -*- coding: utf-8 -*-
"""
    robo.handlers.google_image
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Search image from Google.

    Porting from
    `ruboty-google_image <https://github.com/r7kamura/ruboty-google_image>`_.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import random
import requests
import simplejson as json
from robo.decorators import cmd

logger = logging.getLogger('robo')


class Client(object):
    #: Search animation gif from tumblr.
    GOOGLE_IMAGE_URL = 'https://www.googleapis.com/customsearch/v1'

    def __init__(self):
        self.apikey = os.environ.get('ROBO_GOOGLE_CSE_KEY', None)
        if self.apikey is None:
            raise Exception('ROBO_GOOGLE_CSE_KEY')

        self.cseid = os.environ.get('ROBO_GOOGLE_CSE_ID', None)
        if self.cseid is None:
            raise Exception('ROBO_GOOGLE_CSE_ID')

    def generate(self, query=None):
        """Generate lgtm uri.

        :param query: Search query
        """
        if query is None:
            query = 'cat'
        try:
            url = self.search_resource(query)
            if url:
                return url['unescapedUrl']
        except Exception as e:
            logger.error('Error raised. Query is {0}'.format(query))
            logger.exception(e)
            return None

    def search_resource(self, query):
        """Search image resource from Google image.

        :param query: Search query
        """
        params = {
            'rsz': 8,
            'safe': 'active',
            'cx': self.cseid,
            'key': self.apikey,
            'q': query
        }

        res = requests.get(self.GOOGLE_IMAGE_URL, params=params)
        if res.status_code == 200:
            body = json.loads(res.content)
            resource = random.choice(body['responseData']['results'])

            return resource

        return None


class GoogleImage(object):
    def __init__(self):
        #: Change requests log level.
        logging.getLogger('requests').setLevel(logging.ERROR)
        self.client = Client()

    @cmd(regex=r'image( me)? (?P<keyword>.+)',
         description='Search image from Google.')
    def get(self, message, **kwargs):
        return self.client.generate(message.match.group(2))
