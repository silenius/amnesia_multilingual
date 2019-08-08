
# -*- coding: utf-8 -*-

from sqlalchemy import orm

from amnesia.modules.content_type.utils import get_type_id
from amnesia.modules.file import File
from amnesia_multilingual.modules.content import ContentTranslation
from amnesia_multilingual.modules.file import FileTranslation


def includeme(config):
    tables = config.registry['metadata'].tables

    config.include('amnesia_multilingual.modules.content.mapper')
    config.include('amnesia.modules.file.mapper')

    orm.mapper(
        FileTranslation,
        tables['amnesia_multilingual.content_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'file'),
        properties={
            'content': orm.relationship(
                File, innerjoin=True, uselist=False
            )
        }
    )
