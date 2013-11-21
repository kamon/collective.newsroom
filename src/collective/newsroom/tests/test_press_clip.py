# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager
from zope.component import queryMultiAdapter
import unittest2 as unittest

from Products.Five.browser import BrowserView as View

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.textfield.value import RichTextValue

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from collective.newsroom.interfaces import IPressClip

from collective.newsroom.testing import COLLECTIVE_NEWSROOM_INTEGRATION_TESTING


from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer


class PressClipIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_NEWSROOM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        from collective.newsroom.interfaces import (
            ICollectiveNewsRoomLayer
        )
        alsoProvides(self.request, ICollectiveNewsRoomLayer)
        alsoProvides(self.request, IPloneFormLayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name='PressClip')
        schema = fti.lookupSchema()
        #print schema.getName()
        self.assertEqual(schema.getName(), 'plone_0_PressClip')

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='PressClip'
        )
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='PressClip'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPressClip.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'PressClip',
            'doc1'
        )
        self.assertTrue(IPressClip.providedBy(self.portal['doc1']))

