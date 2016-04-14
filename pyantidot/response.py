from bunch import Bunch as BaseBunch

from pyantidot.exception import NotFoundException


class Bunch(BaseBunch):
    def __getattr__(self, k):
        value = super(Bunch, self).__getattr__(k)
        if type(value) is dict:
            return Bunch(value)
        if type(value) is list:
            for key, list_item in enumerate(value):
                if type(list_item) is dict:
                    value[key] = Bunch(list_item)
        return value


class Response(Bunch):
    @property
    def facets(self):
        return self.replySet[0].facets.facet

    def facet(self, facet_id):
        for facet in self.facets:
            if facet.id == facet_id:
                return FacetTree(facet)
        raise NotFoundException('facet "{0}" not found in response'.format(facet_id))

    @property
    def contents(self):
        return [Content(reply) for reply in self.replySet[0].content.reply]


class FacetTree(Bunch):
    @property
    def nodes(self):
        return [FacetNode(node) for node in self.node]

    def node_(self, key):
        for node in self.nodes:
            if node.key == key:
                return FacetNode(node)
        raise NotFoundException('FacetNode not found for key "{0}"'.format(key))


class FacetNode(Bunch):
    def label(self, lang):
        for label in self.labels:
            if label.lang == lang:
                return label.label
        raise NotFoundException('Lang "{0}" not found for FacetNode "{1}, langs availables: {2}'
                                .format(lang, self.key, 'TODO'))

    @property
    def items(self):
        """ Override of dict .items() method """
        return self['items']


class Content(Bunch):
    pass
