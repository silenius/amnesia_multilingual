# -*- coding: utf-8 -*-

from amnesia.modules.document import Document
from amnesia_multilingual.modules.document import DocumentTranslation


def includeme(config):
    config.include('amnesia_multilingual.modules.content.config')
    config.include('.mapper')

    config.set_translatable_mapping(Document, DocumentTranslation)
    config.set_translatable_attrs(Document, ('title', 'description', 'body',
                                             'fts' ))
