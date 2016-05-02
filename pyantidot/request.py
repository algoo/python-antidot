# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
from werkzeug.datastructures import MultiDict

from pyantidot.response import Response
from pyantidot.tools import Bunch


class Request(object):
    _web_service_name = NotImplemented
    _defaults = {}
    _forced = {
        'output': 'json,3'
    }

    def __init__(self, url, service):
        self._url = url
        self._service = service

    @property
    def service_address(self):
        return '{0}/{1}'.format(self._url, self._web_service_name)

    def get(self, parameters: MultiDict):
        parameters.update(self._defaults)
        parameters.update({
            'service': self._service
        })
        parameters.update(self._forced)
        parameters = [('afs:{0}'.format(key), value) for key, value in parameters.items(True)]

        url = '{0}?{1}'.format(self.service_address, urlencode(parameters))

        response = requests.get(url)
        return Response(Bunch(response.json()))


class SearchRequest(Request):
    _web_service_name = 'search'
