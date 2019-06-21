# -*- coding: utf-8 -*-

from amnesia.modules.event import Event
from amnesia_multilingual.modules.event import EventTranslation


def includeme(config):
    '''Pyramid includeme'''
    config.include('amnesia_multilingual.modules.content.config')
    config.include('.mapper')

    config.set_translatable_mapping(Event, EventTranslation)
    config.set_translatable_attrs(Event, ('title', 'description', 'body',
                                          'fts'))
