# -*- coding: utf-8 -*-

import transaction

from plone.dexterity.content import Item
from plone.dexterity.content import Container

from Products.CMFPlone.i18nl10n import utranslate

from zope.interface import implements

from collective.newsroom.interfaces import (
    IPressRelease,
    IPressClip,
    INewsRoom,
)

# Improve later... by using a better API
from Products.CMFPlone.utils import _createObjectByType
from plone.app.contenttypes.setuphandlers import (
    _setup_constrains,
    _publish,
)

class PressRelease(Item):
    implements(IPressRelease)


class PressClip(Item):
    implements(IPressClip)




def addCollectionAsListingPage(container, title, added_content_types):
    _createObjectByType('Collection', container,
                        id='aggregator', 
                        title=title,
                        #description=description
                        )
                                                    
    aggregator = container['aggregator']

    container.setOrdering('unordered')
    container.setDefaultPage('aggregator')

    # Set the Collection criteria.
    #: Sort on the Effective date
    aggregator.sort_on = u'effective'
    aggregator.reverse_sort = True
    #: Query by Type, Review State, Date, etc.
    query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': added_content_types,
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.is',
             'v': [u'published'],
             },
        ]
    aggregator.query = query

    aggregator.setLayout('summary_view')

    _publish(aggregator)


class NewsRoom(Container):
    implements(INewsRoom)
    
    def _createSubObjects(self):
        """ """

        if 'press-releases' not in self.objectIds():
            self.invokeFactory("Folder", 'press-releases')
            obj = self['press-releases']

            obj.setTitle(utranslate('newsroom', 'Press Releases', context=self))
            obj.setDescription(utranslate('pressroom', 'Our press releases', context=self))
            
            addCollectionAsListingPage(obj, obj.Title(), ['PressRelease'])
            _setup_constrains(obj, ['PressRelease'])

            _publish(obj)
            obj.reindexObject()

        if 'press-clips' not in self.objectIds():
            self.invokeFactory("Folder", 'press-clips')
            obj = self['press-clips']

            obj.setTitle(utranslate('newsroom', 'Press Clips', context=self))
            obj.setDescription(utranslate('pressroom', 'Our press clips', context=self))

            addCollectionAsListingPage(obj, obj.Title(), ['PressClip'])
            _setup_constrains(obj, ['PressClip'])


            _publish(obj)
            obj.reindexObject()

        if 'press-contacts' not in self.objectIds():

            # The Press Contacts directory settings...
            # FIXME: Look for the conventional position types...
            position_types = [{'name': u'Journalist', 'token': u'journalist'},
                              {'name': u'Communication Officer', 'token': u'communication_officer'},
                              {'name': u'Principal', 'token': u'principal'},
                             ]

            # FIXME: Look for the conventional organization types...
            organization_types = [{'name': u'Media House', 'token': u'media_house'},
                                  {'name': u'PR Agency', 'token': u'pr_agency'},
                                  {'name': u'Internal Marketing Department', 'token': u'internal_marketing_department'},
                                 ]

            # FIXME: Do we need this ? Make it optional or find a meaningful org level ?
            organization_levels = [{'name': u'Any', 'token': u'any'},
                                  ]

            params = {'title': u"Press Contacts",
              'position_types': position_types,
              'organization_types': organization_types,
              'organization_levels': organization_levels,
              }
        
            self.invokeFactory('directory', 'press-contacts', **params)
            directory = self['press-contacts']

            _publish(directory)

        transaction.savepoint()
