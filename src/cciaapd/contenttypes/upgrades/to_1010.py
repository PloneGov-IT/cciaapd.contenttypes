# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.referenceablebehavior.uidcatalog import modified_handler
import logging


def update_cciaapd_contenttypes(context, logger=None):
    """Performs the profile update
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cciaapd.contenttypes')

    catalog = getToolByName(context, 'portal_catalog')

    offices_list = catalog.searchResults({'portal_type': 'Ufficio'})
    for office in offices_list:
        logger.info("Updated item %s" % office)
        modified_handler(office.getObject(), None)

    logger.info("Profile updated.")
