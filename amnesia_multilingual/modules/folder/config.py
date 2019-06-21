# -*- coding: utf-8 -*-

from amnesia.modules.folder import Folder
from amnesia_multilingual.modules.folder import FolderTranslation


def includeme(config):
    config.include('amnesia_multilingual.modules.content.config')
    config.include('.mapper')

    config.set_translatable_mapping(Folder, FolderTranslation)
    config.set_translatable_attrs(Folder, ('title', 'description', 'fts'))
