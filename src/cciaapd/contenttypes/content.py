# -*- coding: utf-8 -*-
from zope.interface import implementer
from interfaces import IScheda
from plone.dexterity.content import Container


@implementer(IScheda)
class Scheda(Container):

    """Convenience subclass for ``Collection`` portal type
    """
