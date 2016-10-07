# -*- coding: utf-8 -*-

import bs4
from pyantidot.exception import NotFoundException
from pyantidot.helpers import highlight
from pyantidot.tools import Bunch

DEFAULT_ACP_FEED_NAME = '__DEFAULT__'


class BunchContainer(object):
    def __init__(self, bunch: Bunch):
        self._bunch = bunch

    def get_raw(self):
        return self._bunch


class Labels(list):
    def get(self, lang: str):
        for label_bunch in iter(self):
            if label_bunch.lang == lang:
                return label_bunch.label
        raise NotFoundException()

    def all(self) -> [dict]:
        return iter(self)


class Pager(BunchContainer):
    @property
    def current_page(self) -> int:
        return int(self._bunch.currentPage)

    @property
    def next_page(self):
        return int(self._bunch.nextPage)

    @property
    def previous_page(self):
        return int(self._bunch.previousPage)

    @property
    def pages(self) -> [int]:
        return self._bunch.page

    @property
    def page_nb(self) -> [int]:
        return len(self._bunch.page)


class HighlightText(BunchContainer):
    @property
    def is_match(self) -> bool:
        return 'match' in self._bunch and 'text' not in self._bunch

    @property
    def is_truncate(self) -> bool:
        return ('afs:t' in self._bunch and self._bunch['afs:t'] == 'KwicTruncate')  # nopep8

    def __str__(self) -> str:
        if self.is_match:
            return self._bunch.match
        if self.is_truncate:
            return '...'  # TODO: permettre de personaliser
        return self._bunch.text


class HighlightTextList(list):
    def __str__(self) -> str:
        return ' '.join(map(str, self))

    def get_highlight_text(self, surround) -> str:
        return highlight(self, surround)


class Content(BunchContainer):
    @property
    def doc_id(self) -> int:
        return int(self._bunch.docId)

    @property
    def uri(self) -> str:
        return self._bunch.uri

    @property
    def title(self) -> HighlightTextList:
        return HighlightTextList(
            [HighlightText(bunch) for bunch in self._bunch.title]
        )

    @property
    def abstract(self) -> HighlightTextList:
        return HighlightTextList(
            [HighlightText(bunch) for bunch in self._bunch.abstract]
        )

    @property
    def relevance(self) -> Bunch:
        return self._bunch.relevance

    @property
    def client_data(self) -> [Bunch]:
        return [bunch for bunch in self._bunch.clientData]

    def cdata(self, id) -> str:
        """extract client data without afs tags"""
        for bunch in self.client_data:
            if bunch.id == id:
                return bs4.BeautifulSoup(bunch.contents).text
        return ''

    def cdata_raw(self, id) -> str:
        """extract client data with afs tags"""
        for bunch in self.client_data:
            if bunch.id == id:
                return bunch.contents
        return ''


class ReplySetNode(BunchContainer):
    @property
    def key(self) -> object:
        return self._bunch.key

    @property
    def labels(self) -> Labels:
        if 'labels' not in self._bunch:
            return {}
        return Labels([label for label in self._bunch.labels])

    @property
    def items(self) -> int:
        return int(self._bunch['items'])
        # We can't use self._bunch.items function here,
        # because Bunch.items is a function


class ReplySetFacet(BunchContainer):
    @property
    def layout(self) -> str:
        return self._bunch.layout

    @property
    def type(self) -> str:
        return self._bunch.type

    @property
    def id(self) -> int:
        return self._bunch.id

    @property
    def nodes(self) -> [ReplySetNode]:
        return [ReplySetNode(node) for node in self._bunch.node]

    @property
    def pager(self) -> Pager:
        if 'pager' not in self._bunch:
            return Pager(Bunch({
                'currentPage': 0,
                'nextPage': 0,
                'pages': []
            }))
        return Pager(self._bunch.pager)

    @property
    def labels(self) -> Labels:
        return Labels([label for label in self._bunch.labels])

    def node(self, key: object) -> ReplySetNode:
        for node_bunch in self._bunch.node:
            if node_bunch.key == key:
                return ReplySetNode(node_bunch)
        raise NotFoundException()

class ReplySetMeta(BunchContainer):
    @property
    def uri(self) -> str:
        return self._bunch.uri

    @property
    def total_items(self) -> int:
        return self._bunch.totalItems

    @property
    def total_items_is_exact(self) -> bool:
        return self._bunch.totalItemsIsExact

    @property
    def page_items(self) -> int:
        return self._bunch.pageItems

    @property
    def first_page_item(self) -> int:
        return self._bunch.firstPageItem

    @property
    def last_page_item(self) -> int:
        return self._bunch.lastPageItem

    @property
    def duration_ms(self) -> int:
        return self._bunch.durationMs

    @property
    def first_paf_id(self) -> int:
        return self._bunch.firstPaFId

    @property
    def last_paf_id(self) -> int:
        return self._bunch.lastPaFId

    @property
    def producer(self) -> int:
        return self._bunch.producer


class ReplySet(BunchContainer):
    @property
    def contents(self) -> [Content]:
        return [Content(bunch) for bunch in self._bunch.content.reply]

    @property
    def meta_bunch(self) -> Bunch:
        return self._bunch.meta

    @property
    def meta(self) -> ReplySetMeta:
        return ReplySetMeta(self._bunch.meta)

    @property
    def pager(self) -> Pager:
        if 'pager' not in self._bunch:
            return Pager(Bunch({
                'currentPage': 0,
                'nextPage': 0,
                'pages': []
            }))
        return Pager(self._bunch.pager)

    @property
    def facets(self) -> [ReplySetFacet]:
        return [ReplySetFacet(bunch) for bunch in self._bunch.facets.facet]

    def content(self, uri: object) -> Content:
        for content_bunch in self._bunch.content.reply:
            if content_bunch.uri == uri:
                return Content(content_bunch)
        raise NotFoundException()

    def have_facet(self, id_: object) -> bool:
        try:
            self.facet(id_)
            return True
        except NotFoundException:
            return False

    def facet(self, id_: object) -> ReplySetFacet:
        for facet in self._bunch.facets.facet:
            if facet.id == id_:
                return ReplySetFacet(facet)
        raise NotFoundException()


class HeaderQuery(BunchContainer):
    @property
    def user_id(self):
        return self._bunch.userId

    @property
    def text_query(self):
        return self._bunch.textQuery

    @property
    def session_id(self):
        return self._bunch.sessionId

    @property
    def date(self):
        return self._bunch.date

    @property
    def main_context_bunch(self) -> Bunch:
        return self._bunch.mainCtx

    @property
    def query_param_bunch(self) -> Bunch:
        return self._bunch.queryParam


class Header(BunchContainer):
    @property
    def query_bunch(self) -> Bunch:
        return self._bunch.query

    @property
    def user_bunch(self) -> Bunch:
        return self._bunch.user

    @property
    def performance_bunch(self) -> Bunch:
        return self._bunch.performance

    @property
    def info_bunch(self) -> Bunch:
        return self._bunch.info

    @property
    def query(self) -> HeaderQuery:
        return HeaderQuery(self._bunch.query)


class SearchResponse(BunchContainer):
    @property
    def header(self) -> Header:
        return Header(self._bunch.header)

    @property
    def replies(self) -> list:
        if 'replySet' not in self._bunch:
            return []
        return [ReplySet(bunch) for bunch in self._bunch.replySet]

    def reply(self, uri: object) -> ReplySet:
        if 'replySet' not in self._bunch:
            raise NotFoundException()

        for reply_set_bunch in self._bunch.replySet:
            if reply_set_bunch.meta.uri == uri:
                return ReplySet(reply_set_bunch)

        raise NotFoundException()


class ACPReply(object):
    def __init__(self, index, label, reply_set, data=None):
        self._index = index
        self._label = label
        self._reply_set = reply_set
        self.data = data

    @property
    def label(self):
        return self._label

    @property
    def options_bunch(self):
        try:
            return Bunch(self._reply_set.get_raw()[2][self._index])
        except IndexError:
            return Bunch({})

    def __str__(self):
        return self.label


class ACPReplySet(object):
    def __init__(self, name, bunch):
        self._bunch = bunch
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def query(self):
        try:
            return self._bunch[0]
        except IndexError:
            return None

    @property
    def replies(self) -> [ACPReply]:
        try:
            replies = []
            for index, label in enumerate(self._bunch[1]):
                data = Bunch()
                if len(self._bunch) >= 3:
                    data = self._bunch[2][index]

                replies.append(ACPReply(index, label, self, data=data))

            return replies

        except KeyError:
            return []

    def get_raw(self):
        return self._bunch


class ACPResponse(BunchContainer):
    @property
    def replies_sets(self) -> list:
        return [
            ACPReplySet(name, bunch)
            for name, bunch
            in self._bunch.items()
        ]

    def reply_set(self, name: str, raise_: bool=True) -> ReplySet:
        for key, bunch in self._bunch.items():
            if key == name:
                return ACPReplySet(name, bunch)

        if raise_:
            raise NotFoundException()

        return ACPReplySet(name, Bunch([]))

    @property
    def is_default_reply_set(self):
        return len(self._bunch) and DEFAULT_ACP_FEED_NAME in self._bunch
