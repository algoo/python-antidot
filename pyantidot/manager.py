# -*- coding: utf-8 -*-
import collections
import re

from werkzeug.datastructures import MultiDict

from pyantidot.request import SearchRequest
from pyantidot.response import Response


class Manager(object):
    def __init__(self, api_url: str, service: int):
        self._search_request = SearchRequest(api_url, service=service)

    def collect_query_parameters(self, parameters: MultiDict, bind: dict = None) -> MultiDict:
        builder = QueryParametersBuilder(bind)
        return builder.build(parameters)

    def search(self, parameters: MultiDict=None, **kwargs) -> Response:
        parameters.update(kwargs)
        return self._search_request.get(parameters)


class QueryParametersBuilder(object):
    def __init__(self, bind: dict = None):
        self._bind = bind or {'^query$': ('query', '{value}')}

    def build(self, parameters: MultiDict) -> MultiDict:
        query_parameters = MultiDict()

        for convert_name, convert_value in self._get_bound_parameters(parameters):
            query_parameters.add(convert_name, convert_value)

        return query_parameters

    def _get_bound_parameters(self, parameters: dict):
        for search_param_name, search_param_convert in self._bind.items():
            search_param_convert_name, search_param_convert_value = search_param_convert
            for parameter_name, parameter_value in list(parameters.items()):
                matches = re.search(search_param_name, parameter_name)
                if matches is not None:
                    if not matches.groups():  # expression matches but no groups defined
                        yield search_param_convert_name, search_param_convert_value.format(value=parameter_value)
                    else:  # expression matches with groups defined e.g. ^([a-zA-Z-_]+)_foo$
                        yield (search_param_convert_name.format(*matches.groups()),
                               search_param_convert_value.format(*matches.groups(), value=parameter_value))
