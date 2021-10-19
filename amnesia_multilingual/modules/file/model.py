# -*- coding: utf-8 -*-

from amnesia_multilingual.modules.content import ContentTranslation


class FileTranslation(ContentTranslation):
    ''' Holds File translations '''

    def get_hashid(self, *args, **kwargs):
        return self.content.get_hashid(*args, **kwargs)

    @property
    def extension(self):
        return self.content.extension

    @property
    def alnum_fname(self):
        return self.content.alnum_fname

