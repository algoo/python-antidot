# -*- coding: utf-8 -*-
from pyantidot.request import SearchRequest
from pyantidot.response import Response, Header, ReplySet, ReplySetFacets, Content, ReplySetFacet
from pyantidot.tools import Bunch


def test_search_types():
    # http://training-dev.afs-antidot.net/search?afs:service=2&afs:feed=MARVEL_CHARACTERS&afs:query=hulk
    search = SearchRequest('training-dev.afs-antidot.net', service=2)
    response = search.get(feed='MARVEL_CHARACTERS', query='hulk')

    assert type(response) is Response

    assert type(response.header) is Header
    assert type(response.header.query_bunch) is Bunch
    assert type(response.header.user_bunch) is Bunch
    assert type(response.header.performance_bunch) is Bunch
    assert type(response.header.info_bunch) is Bunch

    assert type(response.replies) is list
    assert type(response.replies[0]) is ReplySet
    assert type(response.reply('MARVEL_CHARACTERS')) is ReplySet
    characters_reply = response.reply('MARVEL_CHARACTERS')

    assert type(characters_reply.meta_bunch) is Bunch
    assert type(characters_reply.contents) is list
    assert type(characters_reply.contents[0]) is Content
    assert type(characters_reply.content(uri='1009351')) is Content
    assert type(characters_reply.pager_bunch) is Bunch
    assert type(characters_reply.facets) is list
    assert type(characters_reply.facets[0]) is ReplySetFacet
    assert type(characters_reply.facet('char_name')) is ReplySetFacet
