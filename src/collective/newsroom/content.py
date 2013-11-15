# -*- coding: utf-8 -*-
from collective.newsroom.interfaces import (
    IPressRelease,
)

from plone.dexterity.content import Item
from plone.dexterity.content import Container

from zope.interface import implements


class PressRelease(Item):
    implements(IPressRelease)


