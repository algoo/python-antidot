# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
from werkzeug.datastructures import MultiDict

from pyantidot.response import SearchResponse, ACPResponse
from pyantidot.tools import Bunch, NotImplementedAttribute


class Request(object):
    _web_service_name = NotImplementedAttribute
    _response_class = NotImplementedAttribute
    _defaults = {}
    _forced = {}

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
        try:
            return self._response_class(Bunch(response.json()))
        except ValueError:
            # When json response is tiny (or ?) like '["hell",[]]' Bunch can't
            # be construct
            return self._response_class(Bunch({}))


class SearchRequest(Request):
    _response_class = SearchResponse
    _web_service_name = 'search'
    _forced = {
        'output': 'json,3'
    }


class ACPRequest(Request):
    _response_class = ACPResponse
    _web_service_name = 'acp'
