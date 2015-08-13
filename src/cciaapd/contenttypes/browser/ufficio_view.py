from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class UfficioView(BrowserView):

    template = ViewPageTemplateFile('ufficio.pt')

    def __call__(self):
        """"""
        self.title = 'OK'
        # getattr(self.context, 'hello_name', 'World')''
        return self.template()
