# -*- coding: utf-8 -*-

from .crud import DocumentTranslationCRUD

def includeme(config):
    config.include('.translations')
    config.include('.crud')
