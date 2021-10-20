# -*- coding: utf-8 -*-

import logging

from pyramid.httpexceptions import HTTPNoContent
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPInternalServerError

from pyramid.view import view_defaults
from pyramid.view import view_config

from amnesia.modules.file.validation import FileSchema
from amnesia.modules.file.forms import FileForm
from amnesia.modules.file import utils as file_utils

from amnesia_multilingual.modules.content import ContentTranslationCRUD
from amnesia_multilingual.modules.file import FileTranslationEntity
from amnesia_multilingual.modules.file import FileTranslationManager

log = logging.getLogger(__name__)


def includeme(config):
    config.scan(__name__)


@view_defaults(context=FileTranslationEntity)
class FileTranslationCRUD(ContentTranslationCRUD):

    @view_config(
        request_method='GET', name='edit', accept='text/html',
        renderer='amnesia:templates/file/edit.pt',
        permission='manage_translations'
    )
    def edit(self):
        data = FileSchema(
            only=('title', 'description')
        ).dump(self.context.translation_doc)

        form = FileForm(self.request)
        form_action = self.request.resource_path(
            self.context.translation_doc.content,
            'translations',
            self.context.language.id
        )

        meta = {
            'sections': ('default', )
        }

        data['language_id'] = self.context.language.id

        return {
            'form': form.render(data, meta=meta),
            'form_action': form_action,
            'edit_locale': self.context.language.id
        }

    #########################################################################
    # (C)RUD - CREATE                                                       #
    #########################################################################

    @view_config(
        context=FileTranslationManager,
        request_method='POST',
        renderer='amnesia:templates/file/edit.pt',
        permission='manage_translations'
    )
    def create(self):
        form_data = self.request.POST.mixed()
        schema = FileSchema(context={
            'request': self.request
        }, only=('title', 'description', 'content'))

        try:
            data = schema.load(form_data)
        except ValidationError as error:
            form = FileForm(self.request)
            form_action = self.request.resource_path(
                self.context.content,
                'translations'
            )

            return {
                'form': form.render(form_data, error.messages),
                'form_action': form_action
            }

        data.update({
            'language_id': form_data.get('language_id'),
            'file_size': 0,
            'mime_id': -1,
            'original_name': ''
        })

        new_entity = self.context.create(data)

        if new_entity:
            file_utils.save_to_disk(self.request, new_entity, data['content'])
            location = self.request.resource_url(new_entity.content)
            return HTTPFound(location=location)

        raise HTTPInternalServerError()


    #########################################################################
    # CR(U)D - UPDATE                                                       #
    #########################################################################

    @view_config(
        request_method='POST',
        renderer='amnesia:templates/file/edit.pt',
        permission='manage_translations'
    )
    def update(self):
        form_data = self.request.POST.mixed()
        schema = FileSchema(context={
            'request': self.request
        }, only=('title', 'description', 'content'))

        try:
            data = schema.load(form_data)
        except ValidationError as error:
            form = FileForm(self.request)
            form_action = self.request.resource_path(
                self.context.content,
                'translations',
                self.context.language.id
            )

            return {
                'form': form.render(form_data, error.messages),
                'form_action': form_action
            }

        updated_entity = self.context.update(data)

        if updated_entity:
            file_utils.save_to_disk(self.request, updated_entity,
                data['content'])
            location = self.request.resource_url(updated_entity.content)
            return HTTPFound(location=location)


    @view_config(request_method='DELETE', permission='delete')
    def delete(self):
        return super().delete()
