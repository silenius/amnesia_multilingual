import logging

from pyramid.security import Deny
from pyramid.security import Everyone
from pyramid.settings import aslist
from pyramid.settings import asbool

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

    def __acl__(self):
        yield from self.parent.__acl__()

    @property
    def available_languages(self):
        return aslist(self.settings['available_languages'])

    def untranslated_languages(self):
        # pylint: disable=no-member
        filters = sql.and_(
            Language.id.in_(self.available_languages),
            sql.not_(
                Language.content_translations.any(
                    language_id=Language.id, content_id=self.entity.id
                )
            )
        )

        return self.dbsession.execute(
            sql.select(Language).filter(filters)
        ).scalars().all()


class ContentTranslationEntity(Resource):

    def __init__(self, request, translation_doc, parent):
        super().__init__(request)
        self.translation_doc = translation_doc
        self.parent = parent

    @property
    def __parent__(self):
        return self.parent

    @property
    def __name__(self):
        return self.language.id

    @property
    def entity(self):
        return self.translation_doc.content

    @property
    def language(self):
        return self.translation_doc.language

    def __acl__(self):
        default_locale = self.settings['pyramid.default_locale_name']
        keep_default = asbool(self.settings.get(
            'amnesia_multilingual.keep_default_translation', False
        ))

        if self.language.id == default_locale and keep_default:
            yield Deny, Everyone, 'delete'

    def update(self, data):
        self.translation_doc.feed(**data)

        try:
            self.dbsession.add(self.translation_doc)
            self.dbsession.flush()
            return self.translation_doc
        except DatabaseError:
            return False

    def delete(self):
        try:
            self.dbsession.delete(self.translation_doc)
            self.dbsession.flush()
            return True
        except DatabaseError:
            return False
