# -*- coding: utf-8 -*-

from amnesia.modules.file import File
from amnesia_multilingual.modules.file import FileTranslation


def includeme(config):
    config.include('amnesia_multilingual.modules.content.config')
    config.include('.mapper')

    config.set_translatable_mapping(File, FileTranslation)
    config.set_translatable_attrs(File, ('title', 'description', 'fts'))
