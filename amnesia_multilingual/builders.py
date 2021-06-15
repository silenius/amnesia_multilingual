# -*- coding: utf-8 -*-

import logging

from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

from sqlalchemy import orm
from sqlalchemy import sql
from sqlalchemy.types import String
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property

from amnesia.modules.language import Language

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

    partition_alias = orm.aliased(
        translation_cls, partition
    )

    # First, add properties on the Content-like class

    content_name = content_cls.__name__.lower()

    content_current_translation = (
        '{}_current_translation'.format(content_name)
    )

    content_translations = (
        '{}_translations'.format(content_name)
    )

    is_base_mapper = content_mapper.base_mapper is content_mapper

    content_mapper.add_properties({
        content_current_translation: orm.relationship(
            partition_alias,
            primaryjoin=sql.and_(
                orm.foreign(partition_alias.content_id) == content_cls.id,
                partition.c.index == 1,
            ),
            lazy='noload' if is_base_mapper else 'joined',
            uselist=False,
            innerjoin=True,
            viewonly=True,
            bake_queries=False,
        ),

        content_translations: orm.relationship(
            lambda: translation_cls,
            cascade='all, delete-orphan',
            innerjoin=True,
            lazy='noload' if is_base_mapper else 'select',
            bake_queries=False,
            backref=orm.backref(
                content_name,
                innerjoin=True,
                uselist=False,
            ),
            collection_class=attribute_mapped_collection('language_id')
        )
    })

    language_name = '{}_language'.format(content_name)

    translation_mapper.add_properties({
        language_name: orm.relationship(
            Language,
            lazy='noload' if is_base_mapper else 'select',
            innerjoin=True,
            uselist=False,
            backref=orm.backref(
                content_translations,
                cascade='all, delete-orphan'
            )
        )
    })

    content_cls.translations = getattr(content_cls, content_translations)
    content_cls.current_translation = getattr(content_cls,
                                              content_current_translation)
    translation_cls.language = getattr(translation_cls, language_name)


def setup_hybrids(cls, name, translation_cls,
                  current_locale=get_current_locale, default=None):

    # The "relationship to aliased class" pattern is in use, and this aliased
    # object was private to the setup_relationships() function, so pull it out
    # here so we can use it in a query
    # See: https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#relationship-to-aliased-class
    partition_alias = cls.current_translation.entity.entity

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
        return getattr(partition_alias, name)

    log.info('Adding hybrid attribute: %s.%s', cls, name)

    prop = hybrid_property(fget=_fget, fset=_fset, expr=_expr)

    setattr(cls, name, prop)

