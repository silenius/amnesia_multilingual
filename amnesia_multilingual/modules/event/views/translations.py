from pyramid.view import view_config
from pyramid.view import view_defaults

from amnesia.modules.event.forms import EventForm
from amnesia.views import BaseView

from amnesia_multilingual.modules.event import EventTranslationManager


def includeme(config):
    config.scan(__name__)


@view_defaults(context=EventTranslationManager)
class Translations(BaseView):

    @view_config(request_method='GET', name='', accept='text/html',
                 renderer='amnesia_multilingual:templates/event/translations.pt')
    def index(self):
        return {
            'event': self.context.entity,
        }

    @view_config(request_method='GET', name='browse', accept='text/html',
                 renderer='amnesia_multilingual:templates/event/browse.pt')
    def browse(self):
        return {
            'event': self.context.entity,
            'translations': self.context.entity.translations,
            'untranslated_languages': self.context.untranslated_languages()
        }

    @view_config(
        request_method='GET', name='add_translation', accept='text/html',
        renderer='amnesia:templates/event/edit.pt',
        permission='manage_translations'
    )
    def add_translation(self):
        lang = self.request.GET.getone('lang')
        form = EventForm(self.request)
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
