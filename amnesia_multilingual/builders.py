# -*- coding: utf-8 -*-

import logging

from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

from sqlalchemy import orm
from sqlalchemy import sql
from sqlalchemy.types import String
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property

log = logging.getLogger(__name__)


def get_current_locale():
    request = get_current_request()

    return request.locale_name


def get_default_locale():
    registry = get_current_registry()

    return registry.settings.get('pyramid.default_locale_name', 'en')


def setup_relationships(content_cls, translation_cls,
                        current_locale=get_current_locale,
                        default_locale=get_default_locale):
    '''Helper to setup translations'''

    log.info('Adding translation properties: %s to %s', content_cls,
             translation_cls)

    content_mapper = orm.class_mapper(content_cls)
    translation_mapper = orm.class_mapper(translation_cls)

    current_locale = sql.bindparam(None, callable_=current_locale,
                                   type_=String())

    default_locale = sql.bindparam(None, callable_=default_locale,
                                   type_=String())

    partition = sql.select([
        translation_cls,
        sql.func.row_number().over(
            order_by=[
                sql.desc(translation_cls.language_id == current_locale),
                sql.desc(translation_cls.language_id == default_locale)
            ],
            partition_by=translation_cls.content_id
        ).label('index')
    ], use_labels=True).where(
        sql.and_(
            translation_cls.language_id.in_((current_locale, default_locale))
        )
    ).alias()

    partition_alias = orm.aliased(translation_cls, partition)

    prop_prefix = content_mapper.class_.__name__.lower()
    prop_current_translation = '{}_current_translation'.format(prop_prefix)
    prop_translations = '{}_translations'.format(prop_prefix)

    content_mapper.add_properties({
        prop_current_translation: orm.relationship(
            partition_alias,
            primaryjoin=sql.and_(
                orm.foreign(partition_alias.content_id) == content_cls.id,
                partition.c.index == 1,
            ),
            lazy='joined',
            uselist=False,
            innerjoin=True,
            viewonly=True,
            bake_queries=False,
        ),

        prop_translations: orm.relationship(
            lambda: translation_cls,
            cascade='all, delete-orphan',
            innerjoin=True,
            back_populates='content',
            collection_class=attribute_mapped_collection('language_id')
        )
    })

    content_cls.current_translation = property(
        lambda self: getattr(self, prop_current_translation)
    )

    content_cls.translations = property(
        lambda self: getattr(self, prop_translations)
    )

    if 'content' not in translation_mapper.relationships:
        translation_mapper.add_properties({
            'content': orm.relationship(
                lambda: content_cls,
                back_populates='translations',
                innerjoin=True,
                uselist=False
            ),
        })

def setup_hybrids(cls, name, translation_cls,
                  current_locale=get_current_locale, default=None):

    def _fget(self):
        return getattr(self.current_translation, name, default)

    def _fset(self, value):
        locale_name = current_locale()

        trans = self.translations.setdefault(
            locale_name,
            translation_cls(language_id=locale_name)
        )

        setattr(trans, name, value)

    def _expr(_cls):
        return _cls.current_translation

    log.info('Adding hybrid attribute: %s.%s', cls, name)

    setattr(cls, name, hybrid_property(fget=_fget, fset=_fset, expr=_expr))

