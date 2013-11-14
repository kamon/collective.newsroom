from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class CollectivenewsroomLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.newsroom
        xmlconfig.file(
            'configure.zcml',
            collective.newsroom,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.newsroom:default')

COLLECTIVE_NEWSROOM_FIXTURE = CollectivenewsroomLayer()
COLLECTIVE_NEWSROOM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_NEWSROOM_FIXTURE,),
    name="CollectivenewsroomLayer:Integration"
)
COLLECTIVE_NEWSROOM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_NEWSROOM_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivenewsroomLayer:Functional"
)
