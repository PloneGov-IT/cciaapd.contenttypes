from Products.Five import BrowserView


class UfficioHelperView(BrowserView):

    def get_results(self):
        """ """
        related_office_list = self.context.related_office
        if len(related_office_list) == 0:
            return[]

        return [x.to_object for x in related_office_list]

    def __call__(self):
        """"""
        return self.get_results() or 'No results'
