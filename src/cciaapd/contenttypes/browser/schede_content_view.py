from Products.Five import BrowserView
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot


class SchedeContentView(BrowserView):

    # def portal_type(self):
    #     """Returns a portal type from the query string
    #     """
    #     return self.request.get('portal_type')

    def get_view(self, parent, view_name):
        view = getMultiAdapter(
            (parent, self.request),
            name=view_name
        )
        return view

    def get_default_view_object(self):
        ''' Check for default page and get it from the context
        if default page is not set return None, otherwise the object
        '''
        default_page_method = getattr(self.context, 'getDefaultPage', None)
        if not default_page_method:
            return None
        default_page = default_page_method()
        obj = self.context.get(default_page)
        return obj

    def is_default_view(self):
        """Return true if the default view is set to Scheda"""
        obj = self.get_default_view_object()
        if not obj:
            return False
        return obj.portal_type == 'Scheda'

    def is_scheda(self):
        """Return true if the content is a Scheda"""
        safe_attribute = getattr(self.context, 'portal_type', None)
        if not safe_attribute:
            return

        return self.context.portal_type == "Scheda"

    def find_nephews(self, portal_type, obj=None, original=True):
        '''
        Check inside objects all the filtered types and
        return their children.
        Moreover, parent folders must be traversed to get contents of the
        first one where the default view is set as Scheda, if exists.
        '''
        if obj is None:
            obj = self.context
        children = obj.listFolderContents(
            contentFilter={'portal_type': portal_type}
        )
        results = []
        [results.extend(child.listFolderContents()) for child in children]
        if original:
            obj = self.get_next()
            if obj is not None:
                view = self.get_view(self.get_next(), u'schede_content_view')
                results.extend(view.get_results(portal_type, original=False))

        return sorted(set(results))

    def get_next(self):
        """Find next interesting object in the aq_chain"""
        for obj in self.context.aq_chain[2:]:
            view = self.get_view(obj, u'schede_content_view')

            if view.is_scheda() or view.is_default_view():
                return obj

    def get_results(self, portal_type, original=True):
        """Returns results depending on request and the following logic

        Case 1: a folder with a Scheda set as  default view ->
                return scheda contents filtered by content_types

        Case 2: the context is a Scheda ->
                return the contents of Moduli or Riferimenti according
                to the requeste portal type

        Case 3: as a fallback return an empty list
        """

        if ISiteRoot.providedBy(self.context):
            return []

        if self.is_default_view():
            return self.find_nephews(portal_type,
                                     self.get_default_view_object(),
                                     original)

        if self.is_scheda():
            return self.find_nephews(portal_type, original=original)

        parent = self.get_next()
        if parent is None:
            return []

        view = self.get_view(parent, u'schede_content_view')

        return view.get_results(portal_type)

    # def __call__(self):
    #     """"""
    #     return self.get_results() or 'No results'
