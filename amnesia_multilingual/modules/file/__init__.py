# -*- coding: utf-8 -*-

from .model import FileTranslation
from .resources import FileTranslationManager
from .resources import FileTranslationEntity
from .views import FileTranslationCRUD

def includeme(config):
    config.include('amnesia_multilingual.modules.content')
    config.include('.mapper')
    config.include('.config')
    config.include('.views')
