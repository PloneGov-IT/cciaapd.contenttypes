# coding=utf-8
from .. import _
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from cciaapd.contenttypes.interfaces import ICciaapdContenttypesLayer
from Products.Archetypes.public import ReferenceField
from Products.ATContentTypes.interface import IATContentType
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.CMFCore.permissions import ModifyPortalContent
from rg.prenotazioni.interfaces.prenotazionifolder import IPrenotazioniFolder
from zope.component import adapts
from zope.interface import implements


class CustomReferenceField(ExtensionField, ReferenceField):
    """ A field, storing reference to an object """


class ContentTypeExtender(object):
    adapts(IATContentType)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ICciaapdContenttypesLayer

    _fields = [
        CustomReferenceField(
            "related_office",
            schemata="categorization",
            allowed_types=('Ufficio'),
            relationship='to_office',
            languageIndependent=True,
            multiValued=True,
            widget=ReferenceBrowserWidget(
                label=_(u"label_related_office", default=u"Related office")
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields


class FolderPrenotazioniExtender(object):
    adapts(IPrenotazioniFolder)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ICciaapdContenttypesLayer

    _fields = [
        CustomReferenceField(
            "relatedItems",
            schemata="categorization",
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            languageIndependent=False,
            index='KeywordIndex',
            referencesSortable=True,
            keepReferencesOnCopy=True,
            write_permission=ModifyPortalContent,
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                allow_sorting=True,
                show_indexes=False,
                force_close_on_insert=True,
                label=_(u'label_related_items', default=u'Related Items'),
                description='',
                visible={'edit': 'visible', 'view': 'invisible'},
            ),
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields


relatedItemsField = ReferenceField(
    'relatedItems',
    relationship='relatesTo',
    multiValued=True,
    isMetadata=True,
    languageIndependent=False,
    index='KeywordIndex',
    referencesSortable=True,
    keepReferencesOnCopy=True,
    write_permission=ModifyPortalContent,
    widget=ReferenceBrowserWidget(
        allow_search=True,
        allow_browse=True,
        allow_sorting=True,
        show_indexes=False,
        force_close_on_insert=True,
        label=u'Elementi correlati',
        description='',
        visible={'edit': 'visible', 'view': 'invisible'},
    ),
)
