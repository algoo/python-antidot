from pyantidot.exception import NotFoundException
from pyantidot.tools import Bunch


class BunchContainer(object):
    def __init__(self, bunch: Bunch):
        self._bunch = bunch


class ReplySetFacets(BunchContainer):
    pass


class Content(BunchContainer):
    pass


class ReplySetFacet(BunchContainer):
    pass


class ReplySet(BunchContainer):
    @property
    def facets(self) -> ReplySetFacets:
        return self._bunch.facets

    @property
    def contents(self) -> list:
        return [Content(bunch) for bunch in self._bunch.content.reply]

    @property
    def meta_bunch(self) -> Bunch:
        return self._bunch.meta

    @property
    def pager_bunch(self) -> Bunch:
        return self._bunch.pager

    @property
    def facets(self) -> list:
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


#     @property
#     def facets(self):
#         return Facets(self.replySet[0].facets.facet)
#
#     @property
#     def contents(self):
#         return [Content(reply) for reply in self.replySet[0].content.reply]
#
#     def facet(self, facet_id):
#         for facet in self.facets:
#             if facet.id == facet_id:
#                 return FacetTree(facet)
#         raise NotFoundException('facet "{0}" not found in response'.format(facet_id))
#
#
#
# class FacetTree(Bunch):
#     @property
#     def nodes(self):
#         return [FacetNode(node) for node in self.node]
#
#     def node_(self, key):
#         for node in self.nodes:
#             if node.key == key:
#                 return FacetNode(node)
#         raise NotFoundException('FacetNode not found for key "{0}"'.format(key))
#
#
# class FacetNode(Bunch):
#     def label(self, lang):
#         for label in self.labels:
#             if label.lang == lang:
#                 return label.label
#         raise NotFoundException('Lang "{0}" not found for FacetNode "{1}, langs availables: {2}'
#                                 .format(lang, self.key, 'TODO'))
#
#     @property
#     def items(self):
#         """ Override of dict .items() method """
#         return self['items']
#
#
# class Content(Bunch):
#     pass
