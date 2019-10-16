# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.httpexceptions import HTTPNoContent
from pyramid.view import view_defaults
from pyramid.view import view_config

from amnesia.views import BaseView

from amnesia_multilingual.modules.content import ContentTranslationEntity


def includeme(config):
    config.scan(__name__)


@view_defaults(containment=ContentTranslationEntity)
class ContentTranslationCRUD(BaseView):

    ##########################################################################
    # DELETE                                                                 #
    ##########################################################################

    @view_config(request_method='DELETE', permission='delete')
    def delete(self):
        if self.context.delete():
            return HTTPNoContent()

        raise HTTPInternalServerError()
