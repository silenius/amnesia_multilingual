# -*- coding: utf-8 -*-


from .model import FolderTranslation
from .resources import FolderTranslationManager
from .resources import FolderTranslationEntity
from .views import FolderTranslationCRUD


def includeme(config):
    config.include('amnesia_multilingual.modules.content')
    config.include('.mapper')
    config.include('.config')
    config.include('.views')
