# -*- coding: utf-8 -*-

from .model import FileTranslation


def includeme(config):
    config.include('amnesia_multilingual.modules.content')
    config.include('.mapper')
    config.include('.config')
