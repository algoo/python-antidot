# -*- coding: utf-8 -*-

import json
import logging
import re

from werkzeug.datastructures import MultiDict

from pyantidot.request import SearchRequest
from pyantidot.request import ACPRequest
from pyantidot.request import ACPResponse
from pyantidot.response import SearchResponse

logger = logging.getLogger('pyantidot.manager')

class Manager(object):
    def __init__(
            self,
            api_url: str,
            service: int,
            status: str='stable',
            auto_wildcard: bool=False,
            wildcard_pattern: str='{0}*',
    ):
        self._search_request = SearchRequest(
            api_url,
            service=service,
            status=status
        )
        self._acp_request = ACPRequest(
            api_url,
            service=service,
            status=status
        )
        self._auto_wildcard = auto_wildcard
        self._wildcard_pattern = wildcard_pattern

    def collect_query_parameters(
            self,
            parameters: MultiDict,
            bind: dict=None,
    ) -> MultiDict:
        builder = QueryParametersBuilder(
            bind,
            auto_wildcard=self._auto_wildcard,
            wildcard_pattern=self._wildcard_pattern,
        )
        return builder.build(parameters)

    def search(self, parameters: MultiDict=None, **kwargs) -> SearchResponse:
        parameters.update(kwargs)
        response = self._search_request.get(parameters)
        logger.info('Antidot SEARCH Response: {}'.format(json.dumps(response.get_raw())))  # nopep8
        return response

    def acp(self, parameters: MultiDict=None, **kwargs) -> ACPResponse:
        parameters.update(kwargs)
        response = self._acp_request.get(parameters)
        logger.info('Antidot ACP Response: {}'.format(json.dumps(response.get_raw())))  # nopep8
        return response


class QueryParametersBuilder(object):
    def __init__(
            self,
            bind: dict=None,
            auto_wildcard: bool=False,
            wildcard_pattern: str='{0}*',
    ):
        self._bind = bind or {'^query$': ('query', '{value}')}
        self._auto_wildcard = auto_wildcard
        self._wildcard_pattern = wildcard_pattern

    def build(self, parameters: MultiDict) -> MultiDict:
        query_parameters = MultiDict()

        for convert_name, convert_value in self._get_bound_parameters(
                parameters):
            query_parameters.add(convert_name, convert_value)

        query = query_parameters.get('query')
        if query and self._auto_wildcard:
            terms = query.split(' ')
            wildcards_terms = map(
                lambda term: self._wildcard_pattern.format(term), terms
            )
            query = ' '.join(wildcards_terms)
            query_parameters['query'] = query

        return query_parameters

    def _get_bound_parameters(self, parameters: MultiDict):
        for search_param_name, search_param_convert in self._bind.items():
            search_param_convert_name, search_param_convert_value \
                = search_param_convert
            for parameter_name, parameter_value in list(
                    parameters.items(True)):
                matches = re.search(search_param_name, parameter_name)
                if matches is not None:
                    # expression matches but no groups defined
                    if not matches.groups():
                        yield search_param_convert_name, \
                            search_param_convert_value.format(
                                value=parameter_value
                            )
                    # expression matches with groups defined
                    # e.g. ^([a-zA-Z-_]+)_foo$
                    else:
                        yield (
                            search_param_convert_name.format(
                                *matches.groups()
                            ),
                            search_param_convert_value.format(
                                *matches.groups(),
                                value=parameter_value
                            )
                        )
