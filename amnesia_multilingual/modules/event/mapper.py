from sqlalchemy import orm

from amnesia.db import mapper_registry

from amnesia.modules.content_type.utils import get_type_id
from amnesia.modules.event import Event

from amnesia_multilingual.modules.event import EventTranslation
from amnesia_multilingual.modules.content import ContentTranslation

def includeme(config):
    tables = config.registry['metadata'].tables

    config.include('amnesia_multilingual.modules.content.mapper')
    config.include('amnesia.modules.event.mapper')

    mapper_registry.map_imperatively(
        EventTranslation,
        tables['amnesia_multilingual.event_translation'],
        inherits=ContentTranslation,
        polymorphic_identity=get_type_id(config, 'event'),
    )
