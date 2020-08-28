# -*- coding: utf-8

from pyramid.view import view_config
from pyramid.view import view_defaults

from amnesia.views import BaseView

from amnesia_multilingual.modules.event import EventTranslationManager
from amnesia_multilingual.modules.event import EventTranslationEntity


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
