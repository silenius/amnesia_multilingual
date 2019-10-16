# -*- coding: utf-8 -*-

from .model import DocumentTranslation
from .resources import DocumentTranslationManager
from .resources import DocumentTranslationEntity
from .views import DocumentTranslationCRUD


def includeme(config):
    config.include('amnesia_multilingual.modules.content')
    config.include('.mapper')
    config.include('.config')
    config.include('.views')
