# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.plonesite.testing import COLLECTIVE_PLONESITE_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.plonesite is properly installed."""

    layer = COLLECTIVE_PLONESITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.plonesite is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.plonesite'))

    def test_browserlayer(self):
        """Test that ICollectivePlonesiteLayer is registered."""
        from collective.plonesite.interfaces import (
            ICollectivePlonesiteLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectivePlonesiteLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_PLONESITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.plonesite'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.plonesite is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.plonesite'))

    def test_browserlayer_removed(self):
        """Test that ICollectivePlonesiteLayer is removed."""
        from collective.plonesite.interfaces import \
            ICollectivePlonesiteLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectivePlonesiteLayer,
            utils.registered_layers())
