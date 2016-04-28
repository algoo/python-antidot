# from pyantidot.request import SearchRequest
# from pyantidot.response import FacetTree
# from pyantidot.response import FacetNode


# def test_search_hulk():
#     # http://training-dev.afs-antidot.net/search?afs:service=2&afs:feed=MARVEL_CHARACTERS&afs:query=hulk
#     search = SearchRequest('training-dev.afs-antidot.net', service=2)
#     response = search.get(feed='MARVEL_CHARACTERS', query='hulk')
#
#     # Direct access of response structure
#     assert response.replySet[0].meta.uri == 'MARVEL_CHARACTERS'
#     assert response.replySet[0].meta.totalItems == 15
#
#     # Facets: here .facet is high level function
#     assert len(response.facets) == 2
#     assert response.facet('char_name')
#     assert type(response.facet('char_name')) == FacetTree
#
#     # Facets nodes: some direct response access and high level functions
#     assert response.facet('char_name').nodes
#     assert type(response.facet('char_name').nodes[0]) == FacetNode
#     assert response.facet('char_name').nodes[0].label('FR') == 'A-Bomb (HAS)'
#     assert response.facet('char_name').node_('Hulk').label('FR') == 'Hulk'
#     assert response.facet('char_name').node_('Hulk').items == 1
#
#     # Idem with contents
#     assert len(response.contents) == 10
#     assert response.contents[0].docId == 623
#     assert response.contents[0].uri == '1009351'
#     assert response.contents[0].title[0].match == 'Hulk'
