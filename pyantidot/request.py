# -*- coding: utf-8 -*-
from siesta import API

from pyantidot.response import Response


class Request(object):
    _web_service_name = NotImplemented
    _defaults = {}
    _forced = {
        'output': 'json,3'
    }

    def __init__(self, url, service):
        self._api = API('https://{0}'.format(url))
        self._service = service

    @property
    def service(self):
        return getattr(self._api, self._web_service_name)

    def get(self, **kwargs):
        parameters = self._defaults
        parameters.update(kwargs)
        parameters.update({
            'service': self._service
        })
        parameters.update(self._forced)
        parameters = {'afs:{0}'.format(key): value for key, value in parameters.items()}
        api_response = self.service.get(**parameters)
        return Response(api_response[0].attrs)


class SearchRequest(Request):
    _web_service_name = 'search'
