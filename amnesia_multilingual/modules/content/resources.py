# -*- coding: utf-8 -*-

import logging

from pyramid.security import Deny
from pyramid.security import Everyone
from pyramid.settings import aslist

from sqlalchemy import sql
from sqlalchemy.exc import DatabaseError

from amnesia.resources import Resource
from amnesia.modules.language import Language

log = logging.getLogger(__name__)


class ContentTranslationManager(Resource):

    __name__ = 'translations'

    def __init__(self, request, entity, parent):
        super().__init__(request)
        self.entity = entity
        self.parent = parent

    @property
    def __parent__(self):
        return self.parent

    @property
    def available_languages(self):
        return aslist(self.settings['available_languages'])

    def untranslated_languages(self):
        filters = sql.and_(
            Language.id.in_(self.available_languages),
            sql.not_(
                sql.and_(
                    Language.translations.any(language_id=Language.id,
                                              content_id=self.entity.id)
                )
            )
        )

        return self.dbsession.query(Language).filter(filters).all()


class ContentTranslationEntity(Resource):

    def __init__(self, request, translation_doc, parent):
        super().__init__(request)
        self.entity = translation_doc
        self.parent = parent

    @property
    def __parent__(self):
        return self.parent

    @property
    def __name__(self):
        return self.language.id

    def __acl__(self):
        default_locale = self.settings['pyramid.default_locale_name']
        keep_default = self.settings.get(
            'amnesia_multilingual.keep_default_translation', False
        )

        if self.language.id == default_locale and keep_default:
            yield Deny, Everyone, 'delete'

    @property
    def language(self):
        return self.entity.language

    def delete(self):
        try:
            self.dbsession.delete(self.entity)
            self.dbsession.flush()
            return True
        except DatabaseError:
            return False
