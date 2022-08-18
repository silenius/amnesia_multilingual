import logging

from marshmallow import ValidationError

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPInternalServerError

from pyramid.view import view_defaults
from pyramid.view import view_config

from amnesia.modules.document.validation import DocumentSchema
from amnesia.modules.document.forms import DocumentForm

from amnesia_multilingual.modules.content import ContentTranslationCRUD
from amnesia_multilingual.modules.document import DocumentTranslationEntity
from amnesia_multilingual.modules.document import DocumentTranslationManager

log = logging.getLogger(__name__)


def includeme(config):
    config.scan(__name__)


@view_defaults(context=DocumentTranslationEntity)
class DocumentTranslationCRUD(ContentTranslationCRUD):

    @view_config(
        request_method='GET', name='edit', accept='text/html',
        renderer='amnesia:templates/document/edit.pt',
        permission='manage_translations'
    )
    def edit(self):
        data = DocumentSchema(
            only=('title', 'description', 'body')
        ).dump(self.context.translation_doc)

        form = DocumentForm(self.request)
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
        context=DocumentTranslationManager,
        request_method='POST',
        renderer='amnesia:templates/document/edit.pt',
        permission='manage_translations'
    )
    def create(self):
        form_data = self.request.POST.mixed()
        schema = DocumentSchema(context={
            'request': self.request
        }, only=('title', 'description', 'body'))

        try:
            data = schema.load(form_data)
        except ValidationError as error:
            form = DocumentForm(self.request)
            form_action = self.request.resource_path(
                self.context.entity,
                'translations'
            )

            return {
                'form': form.render(form_data, error.messages),
                'form_action': form_action
            }

        data['language_id'] = form_data.get('language_id')

        new_entity = self.context.create(data)

        if new_entity:
            location = self.request.resource_url(new_entity.content)
            return HTTPFound(location=location)

        raise HTTPInternalServerError()


    #########################################################################
    # CR(U)D - UPDATE                                                       #
    #########################################################################

    @view_config(
        request_method='POST',
        renderer='amnesia:templates/document/edit.pt',
        permission='manage_translations'
    )
    def update(self):
        form_data = self.request.POST.mixed()
        schema = DocumentSchema(context={
            'request': self.request
        }, only=('title', 'description', 'body'))

        try:
            data = schema.load(form_data)
        except ValidationError as error:
            form = DocumentForm(self.request)
            form_action = self.request.resource_path(
                self.context.entity,
                'translations',
                self.context.language.id
            )

            return {
                'form': form.render(form_data, error.messages),
                'form_action': form_action
            }

        updated_entity = self.context.update(data)

        if updated_entity:
            location = self.request.resource_url(updated_entity.content)
            return HTTPFound(location=location)


    #########################################################################
    # DELETE                                                                #
    #########################################################################

    @view_config(request_method='DELETE', permission='delete')
    def delete(self):
        return super().delete()
