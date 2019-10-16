# -*- coding: utf-8 -*-

from .crud import EventTranslationCRUD

def includeme(config):
    config.include('.translations')
    config.include('.crud')
