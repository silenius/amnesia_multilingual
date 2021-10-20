import os.path

from hashids import Hashids

from amnesia_multilingual.modules.content import ContentTranslation
from amnesia.modules.file import File


class FileTranslation(ContentTranslation):
    ''' Holds File translations '''

    @property
    def extension(self):
        return os.path.splitext(self.original_name)[1].lower()

    @property
    def alnum_fname(self):
        file_name, file_ext = os.path.splitext(self.original_name)
        return ''.join(s for s in file_name if s.isalnum()) + file_ext

    def get_hashid(self, salt, min_length=8):
        hashid = Hashids(salt=salt, min_length=min_length)
        return hashid.encode(self.path_name)
