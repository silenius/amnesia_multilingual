# -*- coding: utf-8 -*-

from .model import EventTranslation
from .resources import EventTranslationManager
from .resources import EventTranslationEntity
from .views import EventTranslationCRUD


def includeme(config):
    config.include('amnesia_multilingual.modules.content')
    config.include('.mapper')
    config.include('.config')
    config.include('.views')
