# -*- coding: utf-8 -*-

from nose.tools import eq_
from nose.tools import ok_
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
    search = SearchRequest('http://training-dev.afs-antidot.net', service=2)
    response = search.get(MultiDict((
        ('feed', 'MARVEL_CHARACTERS'),
        ('query', 'hulk'),
    )))

    eq_(type(response), SearchResponse)

    eq_(type(response.header), Header)
    eq_(type(response.header.query_bunch), Bunch)
    eq_(type(response.header.user_bunch), Bunch)
    eq_(type(response.header.performance_bunch), Bunch)
    eq_(type(response.header.info_bunch), Bunch)

    eq_(type(response.replies), list)
    eq_(type(response.replies[0]), ReplySet)
    eq_(type(response.reply('MARVEL_CHARACTERS')), ReplySet)
    characters_reply = response.reply('MARVEL_CHARACTERS')

    eq_(type(characters_reply.meta_bunch), Bunch)
    eq_(type(characters_reply.contents), list)
    eq_(type(characters_reply.contents[0]), Content)
    eq_(type(characters_reply.content(uri='1009351')), Content)
    content = characters_reply.content(uri='1009351')

    eq_(type(characters_reply.pager), Pager)
    eq_(type(characters_reply.facets), list)
    eq_(type(characters_reply.facets[0]), ReplySetFacet)
    eq_(type(characters_reply.facet('char_name')), ReplySetFacet)
    char_name_facet = characters_reply.facet('char_name')

    eq_(type(char_name_facet.pager), Pager)
    eq_(type(char_name_facet.nodes), list)
    eq_(type(char_name_facet.nodes[0]), ReplySetNode)
    eq_(type(char_name_facet.node('A-Bomb (HAS)')), ReplySetNode)
    eq_(type(char_name_facet.labels), Labels)
    eq_(type(char_name_facet.labels[0]), Bunch)
    reply_set_node = char_name_facet.node('A-Bomb (HAS)')

    ok_(isinstance(reply_set_node.key, (str, int)))
    eq_(type(reply_set_node.items), int)
    eq_(type(reply_set_node.labels), Labels)
    eq_(type(reply_set_node.labels[0]), Bunch)

    eq_(type(content.doc_id), int)
    eq_(type(content.uri), str)
    eq_(type(content.title), HighlightTextList)
    eq_(type(content.title[0]), HighlightText)
    eq_(type(content.title[0].is_match), bool)
    eq_(type(str(content.title[0])), str)
    eq_(type(content.abstract), HighlightTextList)
    eq_(type(content.abstract[0]), HighlightText)
    eq_(type(str(content.abstract[0])), str)
    eq_(type(content.relevance), Bunch)
    eq_(type(content.client_data), list)
    eq_(type(content.client_data[0]), Bunch)


def test_acp_types():
    # http://training-dev.afs-antidot.net/acp?afs:service=2&afs:query=hul
    acp = ACPRequest('http://training-dev.afs-antidot.net', service=2)
    response = acp.get(MultiDict((
        ('query', 'hul'),
    )))

    eq_(type(response), ACPResponse)
    eq_(type(response.replies_sets), list)
    eq_(type(response.replies_sets[0]), ACPReplySet)
    eq_(type(response.reply_set('name')), ACPReplySet)
    reply_set = response.reply_set('name')

    eq_(type(reply_set.query), str)
    eq_(type(reply_set.name), str)
    eq_(type(reply_set.replies), list)
    eq_(type(reply_set.replies[0]), ACPReply)
    reply = reply_set.replies[0]

    eq_(type(reply.label), str)
    eq_(type(reply.options_bunch), Bunch)
    eq_(type(reply.options_bunch.thumbnail), str)
