# -*- coding: utf-8 -*-

from .model import ContentTranslation
from .resources import ContentTranslationManager
from .resources import ContentTranslationEntity
from .views import ContentTranslationCRUD


def includeme(config):
    config.include('.mapper')
    config.include('.config')
