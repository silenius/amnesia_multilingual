# -*- coding: utf-8 -*-

import logging

from pyramid.httpexceptions import HTTPNoContent
from pyramid.httpexceptions import HTTPInternalServerError

from pyramid.view import view_defaults
from pyramid.view import view_config

from amnesia_multilingual.modules.content import ContentTranslationCRUD
from amnesia_multilingual.modules.file import FileTranslationEntity

log = logging.getLogger(__name__)


def includeme(config):
    config.scan(__name__)


@view_defaults(context=FileTranslationEntity)
class FileTranslationCRUD(ContentTranslationCRUD):

    @view_config(request_method='DELETE', permission='delete')
    def delete(self):
        return super().delete()
