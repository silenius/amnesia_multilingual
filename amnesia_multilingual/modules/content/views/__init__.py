# -*- coding: utf-8 -*-

from .crud import ContentTranslationCRUD

def includeme(config):
    config.include('.crud')
