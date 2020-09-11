# -*- coding: utf-8 -*-

import logging

from pyramid.settings import aslist

log = logging.getLogger(__name__)

class path_info_lang_tween:

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry

    @property
    def settings(self):
        return self.registry.settings

    @property
    def available_languages(self):
        return aslist(self.settings['available_languages'])

    def __call__(self, request):
        request._script_name = request.script_name
        if not getattr(request, '_LOCALE_', None) in self.available_languages:
            if request.path_info_peek() in self.available_languages:
                lang = request.path_info_pop()
            else:
                lang = self.settings['default_locale_name']

            request._LOCALE_ = lang

        return self.handler(request)
