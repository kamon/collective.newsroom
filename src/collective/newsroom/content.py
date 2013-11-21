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
    INewsRoomItemCollection,
)


class PressRelease(Item):
    implements(IPressRelease)


class PressClip(Item):
    implements(IPressClip)


class NewsRoomItemCollection(Container):
    implements(INewsRoomItemCollection)


class NewsRoom(Container):
    implements(INewsRoom)
    
    def _createSubObjects(self):
        """ """

        if 'press-releases' not in self.objectIds():
            self.invokeFactory("NewsRoomItemCollection", 'press-releases')
            obj = self['press-releases']
            
            obj.setTitle(utranslate('newsroom', 'Press Releases', context=self))
            obj.setDescription(utranslate('pressroom', 'Our press releases', context=self))
            obj.reindexObject()

        if 'press-clips' not in self.objectIds():
            self.invokeFactory("NewsRoomItemCollection", 'press-clips')
            obj = self['press-clips']
            
            obj.setTitle(utranslate('newsroom', 'Press Clips', context=self))
            obj.setDescription(utranslate('pressroom', 'Our press clips', context=self))
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

        transaction.savepoint()
