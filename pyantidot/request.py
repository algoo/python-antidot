# -*- coding: utf-8 -*-

import logging

from urllib.parse import urlencode
import requests
from werkzeug.datastructures import MultiDict

from pyantidot.response import SearchResponse, ACPResponse
from pyantidot.tools import Bunch, NotImplementedAttribute
from pyantidot.response import DEFAULT_ACP_FEED_NAME


logger = logging.getLogger('pyantidot.request')


class Request(object):
    _web_service_name = NotImplementedAttribute
    _response_class = NotImplementedAttribute
    _defaults = {}
    _forced = {}

    def __init__(self, url, service, status: str='stable'):
        self._url = url
        self._service = service
        self._status = status

    @property
    def service_address(self):
        return '{0}/{1}'.format(self._url, self._web_service_name)

    def get(self, parameters: MultiDict):
        parameters.update(self._defaults)
        parameters.update({
            'service': self._service,
            'status': self._status
        })
        parameters.update(self._forced)
        param_list = []
        for key, value in parameters.items(multi=True):
            param_list.append(('afs:{0}'.format(key), value))

        url = '{0}?{1}'.format(self.service_address, urlencode(param_list))
        logger.info('Antidot request: {}'.format(url))
        
        response = requests.get(url)
        object_response = response.json()

        if isinstance(object_response, dict):
            return self._response_class(Bunch(object_response))
        elif isinstance(object_response, list):
            return self._response_class(Bunch({
                DEFAULT_ACP_FEED_NAME: object_response
            }))


class SearchRequest(Request):
    _response_class = SearchResponse
    _web_service_name = 'search'
    _forced = {  # parameters forced on each antidot request
        'output': 'json',
        'output_version': '3'  # nopep8 see https://doc.antidot.net/#/reader/hBAQI4gcOjkYctUMnum4PQ/BvRmoZUPVBxJ1Dj4jx~4Cw
    }


class ACPRequest(Request):
    _response_class = ACPResponse
    _web_service_name = 'acp'
