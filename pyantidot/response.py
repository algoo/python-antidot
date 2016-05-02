from pyantidot.exception import NotFoundException
from pyantidot.helpers import high_light
from pyantidot.tools import Bunch


class BunchContainer(object):
    def __init__(self, bunch: Bunch):
        self._bunch = bunch

    def get_raw(self):
        return self._bunch


class Pager(BunchContainer):
    @property
    def current_page(self) -> int:
        return int(self._bunch.currentPage)

    @property
    def new_page(self):
        return int(self._bunch.currentPage)

    @property
    def pages(self) -> [int]:
        return self._bunch.page


class HighLightText(BunchContainer):
    @property
    def is_match(self) -> bool:
        return 'match' in self._bunch and 'text' not in self._bunch

    @property
    def is_truncate(self) -> bool:
        return 'afs:t' in self._bunch and self._bunch['afs:t'] == 'KwicTruncate'

    def __str__(self) -> str:
        if self.is_match:
            return self._bunch.match
        if self.is_truncate:
            return '...'  # TODO: permettre de personaliser
        return self._bunch.text


class HighLightTextList(list):
    def __str__(self) -> str:
        return ' '.join(map(str, self))

    def get_highlight_text(self, surround) -> str:
        return high_light(self, surround)


class Content(BunchContainer):
    @property
    def doc_id(self) -> int:
        return int(self._bunch.docId)

    @property
    def uri(self) -> str:
        return self._bunch.uri

    @property
    def title(self) -> HighLightTextList:
        return HighLightTextList([HighLightText(bunch) for bunch in self._bunch.title])

    @property
    def abstract(self) -> HighLightTextList:
        return HighLightTextList([HighLightText(bunch) for bunch in self._bunch.abstract])

    @property
    def relevance(self) -> Bunch:
        return self._bunch.relevance

    @property
    def client_data(self) -> [Bunch]:
        return [bunch for bunch in self._bunch.clientData]


class ReplySetNode(BunchContainer):
    @property
    def key(self) -> object:
        return self._bunch.key

    @property
    def labels(self) -> [Bunch]:
        return [label for label in self._bunch.labels]

    @property
    def items(self) -> int:
        return int(self._bunch['items'])  # We can't use self._bunch.items function here, Bunch.items is a function


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
        return Pager(self._bunch.pager)

    @property
    def labels(self) -> [Bunch]:
        return [label for label in self._bunch.labels]

    def node(self, key: object) -> ReplySetNode:
        for node_bunch in self._bunch.node:
            if node_bunch.key == key:
                return ReplySetNode(node_bunch)
        raise NotFoundException()


class ReplySet(BunchContainer):
    @property
    def contents(self) -> [Content]:
        return [Content(bunch) for bunch in self._bunch.content.reply]

    @property
    def meta_bunch(self) -> Bunch:
        return self._bunch.meta

    @property
    def pager(self) -> Pager:
        return Pager(self._bunch.pager)

    @property
    def facets(self) -> [ReplySetFacet]:
        return [ReplySetFacet(bunch) for bunch in self._bunch.facets.facet]

    def content(self, uri: object) -> Content:
        for content_bunch in self._bunch.content.reply:
            if content_bunch.uri == uri:
                return Content(content_bunch)
        raise NotFoundException()

    def facet(self, id: object) -> ReplySetFacet:
        for facet in self._bunch.facets.facet:
            if facet.id == id:
                return ReplySetFacet(facet)
        raise NotFoundException()


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


class Response(BunchContainer):
    @property
    def header(self) -> Header:
        return Header(self._bunch.header)

    @property
    def replies(self) -> list:
        return [ReplySet(bunch) for bunch in self._bunch.replySet]

    def reply(self, uri: object) -> ReplySet:
        for reply_set_bunch in self._bunch.replySet:
            if reply_set_bunch.meta.uri == uri:
                return ReplySet(reply_set_bunch)
        raise NotFoundException()
