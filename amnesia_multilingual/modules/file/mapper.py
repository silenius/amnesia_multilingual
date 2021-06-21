import logging

from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy

from amnesia.db import mapper_registry

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

    mapper_registry.map_imperatively(
        FileTranslation,
        tables['amnesia_multilingual.data_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'file'),
        properties={
            'mime': orm.relationship(
                 Mime, lazy='joined'
            )
        }
    )

    File.mime = association_proxy('file_current_translation', 'mime')
