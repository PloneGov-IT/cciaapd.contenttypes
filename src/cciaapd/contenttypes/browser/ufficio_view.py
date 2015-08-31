from Acquisition import aq_inner
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


class UfficioView(BrowserView):

    @memoize
    def back_references(self):
        ''' Where this expert was related
        '''
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        query = {
            'to_id': intids.getId(aq_inner(self.context)),
            'from_attribute': 'related_office',
        }
        for rel in catalog.findRelations(query):
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result

    def get_field_value(self, field_name):
        return getattr(self.context, field_name, "")
