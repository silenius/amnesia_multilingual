# -*- coding: utf-8 -*-

from amnesia.modules.content import Content
from amnesia_multilingual.modules.content import ContentTranslation


def includeme(config):
    config.set_translatable_mapping(Content, ContentTranslation)
    config.set_translatable_attrs(Content, ('fts', 'title', 'description'))
