# -*- coding: utf-8 -*-

from .crud import FileTranslationCRUD

def includeme(config):
    config.include('.translations')
    config.include('.crud')
