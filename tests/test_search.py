from nose.tools import eq_
from werkzeug.datastructures import MultiDict

from pyantidot.request import SearchRequest


def test_search_hulk():
    # http://training-dev.afs-antidot.net/search?afs:service=2&afs:feed=MARVEL_CHARACTERS&afs:query=hulk
    search = SearchRequest('https://training-dev.afs-antidot.net', service=2)
    response = search.get(MultiDict((
        ('feed', 'MARVEL_CHARACTERS'),
        ('query', 'hulk'),
    )))

    eq_(len(response.replies), 1, 'One reply set in response')

    # Reply set is MARVEL_CHARACTERS
    reply_set = response.reply('MARVEL_CHARACTERS')
    eq_(reply_set.meta_bunch.totalItems, 15, 'Search found 15 results')

    # We have facets in this reply set
    eq_(len(reply_set.facets), 2, 'Reply set own 2 facets')

    # One facet is char_name
    facet = reply_set.facet('char_name')
    eq_(facet.id, 'char_name', 'Facet id is "char_name" but got {}'.format(facet.id))
    eq_(facet.type, 'STRING', 'Facet type is "STRING" but got {}'.format(facet.type))
    eq_(facet.labels[0].label, 'Character name',
        'First facet label is "Character name" but got {}'.format(facet.labels[0].label))
    eq_(facet.labels.get('FR'), 'Character name',
        'First facet label is "Character name" but got {}'.format(facet.labels[0].label))
    eq_(len(facet.nodes), 10, 'Facet contains 10 nodes but got {}'.format(len(facet.nodes)))

    # Facet node
    facet_node = facet.nodes[0]
    eq_(facet_node.key, 'A-Bomb (HAS)', 'First facet node is "A-Bomb (HAS)" but got {}'.format(facet_node.key))

    # We have content in reply set
    eq_(len(reply_set.contents), 10, 'Reply set contain 10 contents but got {}'.format(len(reply_set.contents)))

    # Reply set content
    content = reply_set.contents[0]
    eq_(content.doc_id, 623, 'First content docId is 623 but got'.format(content.doc_id))
    eq_(content.uri, '1009351', 'First content uri is "1009351" but got {}'.format(content.uri))
    eq_(str(content.title), 'Hulk', 'First content title is "Hulk" but got {}'.format(str(content.title)))
    eq_(str(content.abstract), 'Caught in a gamma bomb explosion while trying to save the life of a teenager, '
                               'Dr. Bruce Banner was transformed into the incredibly powerful creature called the  '
                               'Hulk . An all too often misunderstood hero, the angrier the  Hulk  gets, the stronger '
                               'the  Hulk  gets.', 'First content abstract should not be "{}"'
        .format(str(content.abstract)))

    # Content title with high light

    eq_(content.title.get_highlight_text('<strong>{0}</strong>'), '<strong>Hulk</strong>',
        'First content title is "<strong>Hulk</strong>" but got {}'
        .format(content.title.get_highlight_text('<strong>{0}</strong>')))
    eq_(content.abstract.get_highlight_text('<strong>{0}</strong>'),
        'Caught in a gamma bomb explosion while trying to save the life of a teenager, Dr. Bruce Banner was '
        'transformed into the incredibly powerful creature called the <strong>Hulk</strong>. An all too often '
        'misunderstood hero, the angrier the <strong>Hulk</strong> gets, the stronger the <strong>Hulk</strong> gets.',
        'First content abstract should not be {}'.format(content.abstract.get_highlight_text('<strong>{0}</strong>')))
