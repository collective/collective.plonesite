# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.plonesite


class CollectivePlonesiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.plonesite)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.plonesite:default')


COLLECTIVE_PLONESITE_FIXTURE = CollectivePlonesiteLayer()


COLLECTIVE_PLONESITE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PLONESITE_FIXTURE,),
    name='CollectivePlonesiteLayer:IntegrationTesting',
)


COLLECTIVE_PLONESITE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PLONESITE_FIXTURE,),
    name='CollectivePlonesiteLayer:FunctionalTesting',
)


COLLECTIVE_PLONESITE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PLONESITE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectivePlonesiteLayer:AcceptanceTesting',
)
