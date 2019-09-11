# -*- coding: utf-8 -*-

from webob.compat import cgi_FieldStorage

from amnesia.modules.file import File
from amnesia.modules.file.events import FileUpdated
from amnesia_multilingual.modules.file import FileTranslation


def includeme(config):
    config.include('amnesia_multilingual.modules.content.config')
    config.include('.mapper')

    config.set_translatable_mapping(File, FileTranslation)
    config.set_translatable_attrs(File, ('title', 'description', 'fts',
                                         'original_name', 'file_size',
                                         'path_name', 'mime_id'))
    config.add_subscriber(handle_path_name, FileUpdated)


def handle_path_name(event):
    current_locale = event.request.locale_name
    entity_locale = event.entity.current_translation.language_id

    from sqlalchemy import orm

    if entity_locale != current_locale:
        session = orm.object_session(event.entity)
        session.expire(event.entity, ['current_translation'])
