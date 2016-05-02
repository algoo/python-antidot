# -*- coding: utf-8 -*-
from nose.tools import eq_
from werkzeug.datastructures import MultiDict

from pyantidot.manager import Manager


def test_manager_query_builder():
    manager = Manager('training-dev.afs-antidot.net', service=2)

    fixture_args = MultiDict((
        ('query', 'hulk'),
        ('page', '4'),
        ('series_page', '3'),
    ))

    query_parameters = manager.collect_query_parameters(fixture_args, bind={
        '^query$': ('query', '{value}'),
        '^page$': ('page', '{value}'),
        '^([]a-zA-Z-_]+)_page$': ('facet', '{0}, page={value}')
    })

    eq_(query_parameters, MultiDict((
        ('query', 'hulk'),
        ('page', '4'),
        ('facet', 'series, page=3'),
    )))
