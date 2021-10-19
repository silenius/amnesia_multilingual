# -*- coding: utf-8

from pyramid.view import view_config
from pyramid.view import view_defaults

from amnesia.views import BaseView

from amnesia_multilingual.modules.file import FileTranslationManager
from amnesia_multilingual.modules.file import FileTranslationEntity

from amnesia.modules.file.forms import FileForm


def includeme(config):
    config.scan(__name__)


@view_defaults(context=FileTranslationManager)
class Translations(BaseView):

    @view_config(request_method='GET', name='', accept='text/html',
                 renderer='amnesia_multilingual:templates/file/translations.pt')
    def index(self):
        return {
            'file': self.context.entity,
        }

    @view_config(request_method='GET', name='browse', accept='text/html',
                 renderer='amnesia_multilingual:templates/file/browse.pt')
    def browse(self):
        return {
            'file': self.context.entity,
            'translations': self.context.entity.translations,
            'untranslated_languages': self.context.untranslated_languages()
        }

    @view_config(
        request_method='GET', name='add_translation', accept='text/html',
        renderer='amnesia:templates/file/edit.pt',
        permission='manage_translations'
    )
    def add_translation(self):
        lang = self.request.GET.getone('lang')
        form = FileForm(self.request)
        form_action = self.request.resource_path(
            self.context.entity,
            'translations',
        )

        data = {
            'language_id': lang
        }

        meta = {
            'sections': ('default', )
        }

        return {
            'form': form.render(data, meta=meta),
            'form_action': form_action,
        }
