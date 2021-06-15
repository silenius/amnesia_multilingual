import logging

from sqlalchemy import orm
from sqlalchemy import sql

from amnesia.modules.content import Content
from amnesia_multilingual.modules.content import ContentTranslation

log = logging.getLogger(__name__)

def includeme(config):
    tables = config.registry['metadata'].tables
    config.include('amnesia.modules.content.mapper')

    ct = tables['amnesia_multilingual.content_translation']

    orm.mapper(
        ContentTranslation, ct,
        polymorphic_on=sql.select([
            Content.content_type_id
        ]).where(
            ct.c.content_id == Content.id
        ).correlate_except(
            Content
        ).as_scalar()
    )
