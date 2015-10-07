# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from cciaapd.contenttypes import _
from plone.app.textfield import RichText
from zope.schema import TextLine
from zope.schema import Text
from zope import schema
from plone.supermodel import model
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone import api
from Products.CMFCore.interfaces import IFolderish


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


def notify_state_change(self, event):
    set_new_state(self, event.action)


def set_new_state(node, state):
    children = node.listFolderContents()

    for child in children:
        api.content.transition(child, transition=state)
        if IFolderish.providedBy(child):
            set_new_state(child, state)


class IArchivioFolderSchema(model.Schema):

    """ Schema for Archivio """


class IModuliFolderSchema(model.Schema):

    """ Schema for ModuliFolder """


class IRiferimentiFolderSchema(model.Schema):

    """ Schema for RiferimentiFolder """


class IUfficio(Interface):

    """ Marker interface """


class IUfficioSchema(model.Schema):

    location = Text(
        title=_("office_location_label", u"Location"),
        default=u"",
        required=False
    )

    phone = schema.Tuple(
        title=_("office_phone_label", u"Phone"),
        default=(),
        required=False,
        value_type=TextLine(),
        missing_value=(),
    )

    fax = TextLine(
        title=_("office_fax_label", u"Fax"),
        default=u"",
        required=False
    )

    email = TextLine(
        title=_("office_email_label", u"Email"),
        default=u"",
        required=False
    )

    pec = TextLine(
        title=_("office_pec_label", u"Pec"),
        default=u"",
        required=False
    )

    executive = TextLine(
        title=_("office_executive_label", u"Executive"),
        default=u"",
        required=False
    )

    duties = RichText(
        title=_("office_duties_label", u"Duties"),
        default_mime_type='text/html',
        output_mime_type='text/html',
        allowed_mime_types=('text/html', 'text/plain',),
        default=u"",
        required=False
    )
    office_timetable = schema.Tuple(
        title=_("office_timetable_label", u"Timetable"),
        description=_("office_timetable_description", u"One per line."),
        default=(),
        required=False,
        value_type=TextLine(),
        missing_value=(),
    )
