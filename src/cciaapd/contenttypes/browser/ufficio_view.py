from Acquisition import aq_inner
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import referenceable


class UfficioView(BrowserView):

    @memoize
    def back_references(self):
        ''' Return back references both of Dexterity and AT items
        '''

        result = []
        result.extend(self.get_back_references_from_AT_type())
        result.extend(self.get_back_references_from_DX_type())

        return sorted(result, key=lambda x: x.Title())


    def get_back_references_from_AT_type(self):
        """ Returns back references for Archetypes items """

        result = []
        referenceable_item = referenceable.IReferenceable(self.context)
        result.extend(referenceable_item.getBRefs())

        return result

    def get_back_references_from_DX_type(self):
        """ Returns back references for Dexterity items """

        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)

        query = {
            'to_id': intids.getId(aq_inner(self.context)),
            'from_attribute': 'related_office',
        }

        result = []
        for rel in catalog.findRelations(query):
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)

        return result

    def get_field_value(self, field_name):
        return getattr(self.context, field_name, "")

    def html_to_text(self, text):
        if not text:
            return
        portal_transforms = getToolByName(self, 'portal_transforms')
        output = portal_transforms.convert('text_to_html', text).getData()
        return output

    def generate_mail_tag(self, address):
        if not address:
            return ""
        tag = "<a title=\"%s\" href=\"javascript:location.href='"\
              "mailto:'+String.fromCharCode(" % address
        for index, letter in enumerate(address):
            tag += "%s" % ord(letter)
            if index + 1 < len(address):
                tag += ", "
        tag += ")+'?'\">%s</a>" % address
        return tag
