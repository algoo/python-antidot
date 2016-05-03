# -*- coding: utf-8 -*-
from werkzeug.datastructures import MultiDict

from pyantidot.request import ACPRequest


def test_acp_hulk():
    # http://training-dev.afs-antidot.net/acp?afs:service=2&afs:query=hul
    search = ACPRequest('https://training-dev.afs-antidot.net', service=2)
    response = search.get(MultiDict((
        ('query', 'hul'),
    )))

    reply_set = response.reply_set('name')
    assert reply_set.name == 'name'
    assert reply_set.query == 'hul'
    assert reply_set.replies

    reply = reply_set.replies[0]
    assert reply.label == 'Hulk'
    thumb_url = "http://i.annihil.us/u/prod/marvel/i/mg/5/a0/538615ca33ab0.jpg"
    assert reply.options_bunch.thumbnail == thumb_url
