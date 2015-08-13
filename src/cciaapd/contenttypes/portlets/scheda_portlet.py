from .. import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from ..vocs.scheda_types import scheda_types


class ISchedaPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=u"Titolo",
        required=True,
    )

    content_selection = schema.Choice(
        title=_(u'label_disability',
                default=u'Seleziona tipo di contenuto'),
        required=True,
        vocabulary=scheda_types,
    )

    css_class = schema.TextLine(
        title=u"Classe css",
        required=False,
    )


class Assignment(base.Assignment):
    implements(ISchedaPortlet)

    def __init__(self, portlet_title, content_selection, css_class):
        self.portlet_title = portlet_title
        self.content_selection = content_selection
        self.css_class = css_class

    @property
    def title(self):
        return self.portlet_title


class AddForm(base.AddForm):
    form_fields = form.Fields(ISchedaPortlet)
    label = _(u"Add Scheda Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ISchedaPortlet)
    label = _(u"Edit Scheda Portlet")
    description = _(u"")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('scheda_portlet.pt')

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
            return []

        view = getMultiAdapter(
            (context, self.request),
            name=u'schede_content_view'
        )
        return view.get_results(self.data.content_selection)
