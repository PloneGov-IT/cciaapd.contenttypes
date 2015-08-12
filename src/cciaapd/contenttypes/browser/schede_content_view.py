from Products.Five import BrowserView
from zope.component import getMultiAdapter


class SchedeContentView(BrowserView):

    def portal_type(self):
        """Returns a portal type from the query string
        """
        return self.request.get('portal_type')

    def get_default_view_object(self):
        ''' Check for default page and get it from the context
        if default page is not set return None, otherwise the object
        '''
        default_page = self.context.getDefaultPage()
        return self.context.get(default_page)

    def is_default_view(self):
        """Return true if the default view is set to Scheda"""
        obj = self.get_default_view_object()
        if not obj:
            return False
        return obj.portal_type == 'Scheda'

    def is_scheda(self):
        """Return true if the content is a Scheda"""
        return self.context.portal_type == "Scheda"

    def find_nephews(self, obj=None):
        ''' Check inside objects all the filtered types and
        return their children
        '''
        if obj is None:
            obj = self.context
        children = obj.listFolderContents(
            contentFilter={'portal_type': self.portal_type()}
        )
        results = []
        [results.extend(child.listFolderContents()) for child in children]

        parent = self.context.aq_parent
        view = getMultiAdapter(
            (parent, self.request),
            name=u'schede_content_view'
        )
        results.extend(view.get_results())

        return set(results).sort()

    def get_results(self):
        """Returns results depending on request and the following logic

        Case 1: a folder with a Scheda set as  default view ->
                                scheda contents filtered by content_types

        Case 2: the context is a Scheda ->
                return the contents of Moduli or Riferimenti according
                to the requeste portal type

        Fallback: as a fallback return an empty list
        """

        import pdb;pdb.set_trace()

        if self.is_default_view():
            return self.find_nephews(self.get_default_view_object())

        if self.is_scheda():
            return self.find_nephews()

        return []

    def __call__(self):
        """"""
        return self.get_results() or 'No results'
