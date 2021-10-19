# -*- coding: utf-8

from pyramid.view import view_config
from pyramid.view import view_defaults

from amnesia.modules.document.forms import DocumentForm
from amnesia.views import BaseView

from amnesia_multilingual.modules.document import DocumentTranslationManager
from amnesia_multilingual.modules.document import DocumentTranslationEntity


def includeme(config):
    config.scan(__name__)


@view_defaults(context=DocumentTranslationManager)
class Translations(BaseView):

    @view_config(request_method='GET', name='', accept='text/html',
                 renderer='amnesia_multilingual:templates/document/translations.pt')
    def index(self):
        return {
            'document': self.context.entity,
        }

    @view_config(request_method='GET', name='browse', accept='text/html',
                 renderer='amnesia_multilingual:templates/document/browse.pt')
    def browse(self):
        return {
            'document': self.context.entity,
            'translations': self.context.entity.translations,
            'untranslated_languages': self.context.untranslated_languages()
        }

    @view_config(
        request_method='GET', name='add_translation', accept='text/html',
        renderer='amnesia:templates/document/edit.pt',
        permission='manage_translations'
    )
    def add_translation(self):
        lang = self.request.GET.getone('lang')
        form = DocumentForm(self.request)
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
