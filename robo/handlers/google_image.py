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
import logging
import random
import requests
import simplejson as json
from robo.decorators import cmd

logger = logging.getLogger('robo')


class Client(object):
    #: Search animation gif from tumblr.
    GOOGLE_IMAGE_URL = 'http://ajax.googleapis.com/ajax/services/search/images'

    def __init__(self):
        self.resource = None

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
            logger.error(e)
            return None

    def search_resource(self, query):
        """Search image resource from Google image.

        :param query: Search query
        """
        params = {
            'rsz': 8,
            'safe': 'active',
            'v': '1.0',
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
         description='Generate lgtm image matching with the keyword.')
    def get(self, message, **kwargs):
        return self.client.generate(message.match.group(1))
