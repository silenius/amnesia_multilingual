import logging

from sqlalchemy import orm

from amnesia.modules.content_type.utils import get_type_id
from amnesia_multilingual.modules.content import ContentTranslation
from amnesia_multilingual.modules.document import DocumentTranslation

log = logging.getLogger(__name__)


def includeme(config):
    tables = config.registry['metadata'].tables
    config.include('amnesia_multilingual.modules.content.mapper')
    config.include('amnesia.modules.document.mapper')

    orm.mapper(
        DocumentTranslation,
        tables['amnesia_multilingual.document_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'document'),
    )
