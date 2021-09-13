# -*- coding: utf-8 -*-

import logging

from amnesia.modules.language import Language

from amnesia_multilingual.modules.content import ContentTranslationManager
from amnesia_multilingual.modules.content import ContentTranslationEntity
from amnesia_multilingual.modules.file import FileTranslation

log = logging.getLogger(__name__)


class FileTranslationManager(ContentTranslationManager):

    def __init__(self, request, content, parent):
        super().__init__(request, content, parent)

    def __getitem__(self, path):
        if path in self.available_languages:
            tr_doc = self.dbsession.get(FileTranslation, {
                'content_id': self.entity.id,
                'language_id': path
            })

            if tr_doc:
                return FileTranslationEntity(self.request, tr_doc, self)

        raise KeyError

    def query(self):
        return self.dbsession.query(FileTranslation).filter_by(
            content=self.entity)


class FileTranslationEntity(ContentTranslationEntity):
    pass


