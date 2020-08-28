# -*- coding: utf-8 -*-

import logging

from amnesia.modules.language import Language

from amnesia_multilingual.modules.content import ContentTranslationManager
from amnesia_multilingual.modules.content import ContentTranslationEntity
from amnesia_multilingual.modules.folder import FolderTranslation

log = logging.getLogger(__name__)


class FolderTranslationManager(ContentTranslationManager):

    def __init__(self, request, content, parent):
        super().__init__(request, content, parent)

    def __getitem__(self, path):
        if path in self.available_languages:
            tr_doc = self.dbsession.query(FolderTranslation).get({
                'content_id': self.entity.id,
                'language_id': path
            })

            if tr_doc:
                return FolderTranslationEntity(self.request, tr_doc, self)

        raise KeyError

    def query(self):
        return self.dbsession.query(FolderTranslation).filter_by(
            content=self.entity)


class FolderTranslationEntity(ContentTranslationEntity):
    pass


