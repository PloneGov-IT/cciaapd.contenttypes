from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent

class UfficioHelperView(BrowserView):

    def get_results(self):
        """ Returns related offices depending on the type of current item (AT or DX) """

        if IDexterityContent.providedBy(self.context):
            related_office_list = [x.to_object for x in self.context.related_office]
        else:
            related_office_list = self.context.getField("related_office").get(self.context)

        if len(related_office_list) == 0:
            return[]

        return sorted(related_office_list,key=lambda x: x.Title())

    def __call__(self):
        """"""
        return self.get_results() or 'No results'
