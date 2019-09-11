
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy

from amnesia.modules.content_type.utils import get_type_id
from amnesia.modules.file import File
from amnesia.modules.mime import Mime
from amnesia_multilingual.modules.content import ContentTranslation
from amnesia_multilingual.modules.file import FileTranslation

log = logging.getLogger(__name__)


def includeme(config):
    tables = config.registry['metadata'].tables

    config.include('amnesia_multilingual.modules.content.mapper')
    config.include('amnesia.modules.file.mapper')

    orm.mapper(
        FileTranslation,
        tables['amnesia_multilingual.data_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'file'),
        properties={
            'content': orm.relationship(
                File, innerjoin=True, uselist=False
            ),

            'mime': orm.relationship(
                 Mime, lazy='joined'
            )
        }
    )

    File.mime = association_proxy('current_translation', 'mime')
    #File.mime_id = association_proxy('current_translation', 'mime_id')
