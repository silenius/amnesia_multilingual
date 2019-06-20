# -*- coding: utf-8 -*-

from sqlalchemy import orm

from amnesia.modules.content_type.utils import get_type_id
from amnesia_multilingual.modules.content import ContentTranslation
from amnesia_multilingual.modules.folder import FolderTranslation


def includeme(config):
    tables = config.registry['metadata'].tables

    config.include('amnesia_multilingual.modules.content.mapper')
    config.include('amnesia.modules.folder.mapper')

    orm.mapper(
        FolderTranslation,
        tables['content_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'folder')
    )
