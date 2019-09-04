# -*- coding: utf-8 -*-

import logging

from sqlalchemy import event
from sqlalchemy import orm

from pyramid.threadlocal import get_current_registry

from amnesia_multilingual.builders import setup_hybrids
from amnesia_multilingual.builders import setup_relationships

log = logging.getLogger(__name__)

_TRANSLATIONS_KEY = 'amnesia.translations'


def _setup_translation():
    log.debug('SQLAlchemy after_configured handler _setup_translation called')
    registry = get_current_registry()

    if _TRANSLATIONS_KEY not in registry:
        return

    _cfg = registry[_TRANSLATIONS_KEY]

    if 'mappings' in _cfg:
        for cls, tr_cls in _cfg['mappings'].items():
            setup_relationships(cls, tr_cls)

    if 'attrs' in _cfg:
        for cls, cols in _cfg['attrs'].items():
            translation_cls = _cfg['mappings'][cls]
            for col in cols:
                setup_hybrids(cls, col, translation_cls)


def set_translatable_attrs(config, cls, cols):
    _attrs = config.registry.\
        setdefault(_TRANSLATIONS_KEY, {}).\
        setdefault('attrs', {})

    _attrs[cls] = cols


def set_translatable_mapping(config, cls, trans_cls):
    _mappings = config.registry.\
        setdefault(_TRANSLATIONS_KEY, {}).\
        setdefault('mappings', {})

    _mappings[cls] = trans_cls


def includeme(config):
    event.listen(orm.mapper, 'after_configured', _setup_translation)
    config.add_directive('set_translatable_attrs', set_translatable_attrs)
    config.add_directive('set_translatable_mapping', set_translatable_mapping)
    config.add_tween('amnesia_multilingual.tweens.path_info_lang_tween')
