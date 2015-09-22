from .. import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class IArchivioPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=u"Titolo",
        required=True,
    )

    css_class = schema.TextLine(
        title=u"Classe css",
        required=False,
    )


class Assignment(base.Assignment):
    implements(IArchivioPortlet)

    def __init__(self, portlet_title, css_class):
        self.portlet_title = portlet_title
        self.css_class = css_class

    @property
    def title(self):
        return self.portlet_title


class AddForm(base.AddForm):
    form_fields = form.Fields(IArchivioPortlet)
    label = _(u"Add Archivio Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IArchivioPortlet)
    label = _(u"Edit Archivio Portlet")
    description = _(u"")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('archivio_portlet.pt')

    def render(self):
        return self._template()

    @property
    def available(self):
        return len(self._data())

    def results(self):
        return self._data()

    @memoize
    def _data(self):
        context = self.context.aq_inner
        if context.portal_type != 'Scheda':
            return None

        archivio = context.listFolderContents(
            contentFilter={'portal_type': "ArchivioFolder"}
        )
        if not archivio:
            return None
        return archivio[0]
