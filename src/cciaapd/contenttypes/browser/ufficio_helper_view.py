from Products.Five import BrowserView
from plone.dexterity.interfaces import IDexterityContent


class UfficioHelperView(BrowserView):

    def get_results(self):
        """
        Returns related offices depending on the type of current item (AT or DX).
        Omit expired offices
        """
        if IDexterityContent.providedBy(self.context):
            return [x.to_object for x in self.context.related_office if not x.to_object.isExpired()]
        else:
            related_office_field = self.context.getField("related_office")
            if not related_office_field:
                return []
            return [x for x in related_office_field.get(self.context) if not x.isExpired()]
        return []

    def __call__(self):
        """"""
        return self.get_results() or 'No results'
