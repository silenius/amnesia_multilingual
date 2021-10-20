import logging

from sqlalchemy.exc import DatabaseError

from amnesia.modules.language import Language

from amnesia_multilingual.modules.content import ContentTranslationManager
from amnesia_multilingual.modules.content import ContentTranslationEntity
from amnesia_multilingual.modules.file import FileTranslation

log = logging.getLogger(__name__)


class FileTranslationManager(ContentTranslationManager):

    def __init__(self, request, entity, parent):
        super().__init__(request, entity, parent)

    def __getitem__(self, path):
        if path in self.available_languages:
            tr_doc = self.dbsession.get(FileTranslation, {
                'content_id': self.entity.id,
                'language_id': path
            })

            if tr_doc:
                return FileTranslationEntity(self.request, tr_doc, self)

        raise KeyError

    def create(self, data):
        # FIXME
        foo = {k: v for k,v in data.items() if k != 'content'}

        new_translation = FileTranslation(
            content=self.entity, **foo
        )

        try:
            self.dbsession.add(new_translation)
            self.dbsession.flush()
            return new_translation
        except DatabaseError:
            return False


class FileTranslationEntity(ContentTranslationEntity):
    """FileTranslation resource"""


