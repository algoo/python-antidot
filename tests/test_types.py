# -*- coding: utf-8 -*-
from werkzeug.datastructures import MultiDict

from pyantidot.request import SearchRequest, ACPRequest
from pyantidot.response import HighlightTextList
from pyantidot.response import ACPResponse
from pyantidot.response import ACPReplySet
from pyantidot.response import ACPReply
from pyantidot.response import Labels
from pyantidot.response import SearchResponse
from pyantidot.response import Header
from pyantidot.response import ReplySet
from pyantidot.response import Content
from pyantidot.response import ReplySetFacet
from pyantidot.response import Pager
from pyantidot.response import ReplySetNode
from pyantidot.response import HighlightText
from pyantidot.tools import Bunch


def test_search_types():
    # http://training-dev.afs-antidot.net/search?afs:service=2&afs:feed=MARVEL_CHARACTERS&afs:query=hulk
    search = SearchRequest('https://training-dev.afs-antidot.net', service=2)
    response = search.get(MultiDict((
        ('feed', 'MARVEL_CHARACTERS'),
        ('query', 'hulk'),
    )))

    assert type(response) is SearchResponse

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
    content = characters_reply.content(uri='1009351')

    assert type(characters_reply.pager) is Pager
    assert type(characters_reply.facets) is list
    assert type(characters_reply.facets[0]) is ReplySetFacet
    assert type(characters_reply.facet('char_name')) is ReplySetFacet
    char_name_facet = characters_reply.facet('char_name')

    assert type(char_name_facet.pager) is Pager
    assert type(char_name_facet.nodes) is list
    assert type(char_name_facet.nodes[0]) is ReplySetNode
    assert type(char_name_facet.node('A-Bomb (HAS)')) is ReplySetNode
    assert type(char_name_facet.labels) is Labels
    assert type(char_name_facet.labels[0]) is Bunch
    reply_set_node = char_name_facet.node('A-Bomb (HAS)')

    assert isinstance(reply_set_node.key, (str, int))
    assert type(reply_set_node.items) is int
    assert type(reply_set_node.labels) is Labels
    assert type(reply_set_node.labels[0]) is Bunch

    assert type(content.doc_id) is int
    assert type(content.uri) is str
    assert type(content.title) is HighlightTextList
    assert type(content.title[0]) is HighlightText
    assert type(content.title[0].is_match) is bool
    assert type(str(content.title[0])) is str
    assert type(content.abstract) is HighlightTextList
    assert type(content.abstract[0]) is HighlightText
    assert type(str(content.abstract[0])) is str
    assert type(content.relevance) is Bunch
    assert type(content.client_data) is list
    assert type(content.client_data[0]) is Bunch


def test_acp_types():
    # http://training-dev.afs-antidot.net/acp?afs:service=2&afs:query=hul
    acp = ACPRequest('https://training-dev.afs-antidot.net', service=2)
    response = acp.get(MultiDict((
        ('query', 'hul'),
    )))

    assert type(response) is ACPResponse
    assert type(response.replies_sets) is list
    assert type(response.replies_sets[0]) is ACPReplySet
    assert type(response.reply_set('name')) is ACPReplySet
    reply_set = response.reply_set('name')

    assert type(reply_set.query) is str
    assert type(reply_set.name) is str
    assert type(reply_set.replies) is list
    assert type(reply_set.replies[0]) is ACPReply
    reply = reply_set.replies[0]

    assert type(reply.label) is str
    assert type(reply.options_bunch) is Bunch
    assert type(reply.options_bunch.thumbnail) is str
