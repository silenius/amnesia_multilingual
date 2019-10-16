# -*- coding: utf-8 -*-

from .crud import FolderTranslationCRUD

def includeme(config):
    config.include('.translations')
    config.include('.crud')
