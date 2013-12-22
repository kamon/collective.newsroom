# -*- coding: utf-8 -*-
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

#from plone.namedfile import field as namedfile

from collective.newsroom import MessageFactory as _

#from collective.contact.widget.schema import ContactChoice, ContactList
#from collective.contact.widget.source import ContactSourceBinder


## PressRelease Metadata

class IPressReleaseMetadata(model.Schema):

    releaseTiming = schema.TextLine(
        title=_(u"releaseTiming"),
        description=u'''When should this release be distributed (e.g. FOR IMMEDIATE RELEASE and HOLD FOR RELEASE UNTIL MM/DD/YYYY)''',
        required=False,
    )

    releaseLocation = schema.TextLine(
        title=_(u"releaseLocation"),
        description=u'''Typically press releases have an associated location in a common format (i.e. City, State)''',
        required=False,
    )

    releaseDate = schema.Datetime(
        title=_(u"release Date"),
        description=u"Provide a date for when this press release will be distributed",
        required=True,
    )

    #releaseContacts --> see plone.app.relationfield --> relations with PressContact contents.
#     releaseContacts = ContactList(
#         title=_(u"release Contacts"),
#         description=u"",
#         value_type=ContactChoice(
#                     description=_("Search and attach press contacts"),
#                     source=ContactSourceBinder(portal_type=("person",)),),
#         required=False,
#         addlink=False,
#     )
    

alsoProvides(IPressReleaseMetadata, IFormFieldProvider)


class PressReleaseMetadata(object):
    implements(IPressReleaseMetadata)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


## PressClip Metadata

class IPressClipMetadata(model.Schema):

    reporter = schema.TextLine(
        title=_(u"Reporter\'s Name"),
        description=u"Provide the name of the reporter",
        required=False,
    )


alsoProvides(IPressClipMetadata, IFormFieldProvider)


class PressClipMetadata(object):
    implements(IPressClipMetadata)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

