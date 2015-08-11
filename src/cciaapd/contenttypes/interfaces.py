# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from cciaapd.contenttypes import _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICciaapdContenttypesLayer(IDefaultBrowserLayer):

    """Marker interface that defines a browser layer."""


class IScheda(Interface):

    """Marker interface for folderish scheda"""


class ISchedaSchema(model.Schema):

    body_text = RichText(
        title=_(u"Body text"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain',),
        default=u""
    )


class IModuliFolderSchema(model.Schema):

    """ Schema for ModuliFolder """


class IRiferimentiFolderSchema(model.Schema):

    """ Schema for RiferimentiFolder """
