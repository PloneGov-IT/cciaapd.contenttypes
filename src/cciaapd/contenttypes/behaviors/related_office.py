# -*- coding: utf-8 -*-
from .. import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import alsoProvides


class IRelatedOffice(model.Schema):

    ''' Behavior interface
    '''
    form.widget(related_office=MultiContentTreeFieldWidget)
    related_office = RelationList(
        title=_(u'label_related_office', default=u'Related office'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(),
        ),
        required=False
    )


class RelatedOffice(model.Schema):

    ''' Behavior interface
    '''

alsoProvides(IRelatedOffice, IFormFieldProvider)
