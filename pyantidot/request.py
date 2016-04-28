# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests

from pyantidot.response import Response
from pyantidot.tools import Bunch


class Request(object):
    _web_service_name = NotImplemented
    _defaults = {}
    _protocol = 'https'
    _forced = {
        'output': 'json,3'
    }

    def __init__(self, url, service):
        self._api_address = '{0}://{1}'.format(self._protocol, url)
        self._service = service

    @property
    def service_address(self):
        return '{0}/{1}'.format(self._api_address, self._web_service_name)

    def get(self, **kwargs):
        parameters = self._defaults
        parameters.update(kwargs)
        parameters.update({
            'service': self._service
        })
        parameters.update(self._forced)
        parameters = [('afs:{0}'.format(key), value) for key, value in parameters.items()]

        url = '{0}?{1}'.format(self.service_address, urlencode(parameters))

        response = requests.get(url)
        return Response(Bunch(response.json()))


class SearchRequest(Request):
    _web_service_name = 'search'
