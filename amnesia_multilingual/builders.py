# -*- coding: utf-8 -*-

import logging

from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

from sqlalchemy import orm
from sqlalchemy import sql
from sqlalchemy import event
from sqlalchemy.types import String
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property

log = logging.getLogger(__name__)


def _localizer(request=None):
    if not request:
        request = get_current_request()

    return request.locale_name


def setup_relationships(content_cls, translation_cls, localizer=None, **kwargs):
    '''Helper to setup translations'''

    log.debug('Adding translation properties: %s to %s', content_cls,
              translation_cls)

    if not localizer:
        localizer = _localizer

    content_mapper = orm.class_mapper(content_cls)
    translation_mapper = orm.class_mapper(translation_cls)

    partition = sql.select([
        translation_cls,
        sql.func.row_number().over(
            order_by=[
                sql.desc(translation_cls.language_id == sql.bindparam(
                    None, callable_=lambda: localizer(), type_=String()
                )),
                sql.desc(translation_cls.language_id == 'en')
            ],
            partition_by=translation_cls.content_id
        ).label('index')
    ], use_labels=True).where(
        sql.and_(
            translation_cls.language_id.in_((
                sql.bindparam(
                    None, callable_=lambda: localizer(), type_=String()
                ),
                'en'
            ))
        )
    ).alias()

    partition_alias = orm.aliased(translation_cls, partition)

    content_mapper.add_properties({
        'current_translation': orm.relationship(
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
            #back_populates='content'
        ),

        'translations': orm.relationship(
            lambda: translation_cls,
            cascade='all, delete-orphan',
            #lazy='subquery',
            innerjoin=True,
            back_populates='content',
            collection_class=attribute_mapped_collection('language_id')
        )
    })

    if not 'content' in translation_mapper.relationships:
        translation_mapper.add_properties({
            'content': orm.relationship(
                lambda: content_cls,
                back_populates='translations',
                innerjoin=True,
                uselist=False
            ),
        })


def setup_hybrids(cls, name, translation_cls):

    @hybrid_property
    def _column(self):
        return getattr(self.current_translation, name, 'NONE')

    @_column.setter
    def _column(self, value):
        locale_name = _localizer()

        trans = self.translations.setdefault(
            locale_name, translation_cls(language_id=locale_name)
        )

        setattr(trans, name, value)

    #@_column.expression
    #def _column(cls):
    #    return cls.current_translation.has()

    _column.__name__ = name

    return _column
