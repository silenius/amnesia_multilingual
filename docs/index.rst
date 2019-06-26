.. _index:

===========================
Amnesia multilingual plugin
===========================

Amnesia multilingual content plugin provides multi-language support for
Content-based content types in AmnesiaCMS.

=================
How does it work?
=================

Multilingual support for each Content-based content type will be stored in a
dedicated translation table.

=====
Usage
=====

#. Install package:

   .. code-block:: bash

      pip install amnesia_multilingual

#. Create translation table(s):

   .. code-block:: sql

      create table amnesia_translation.document_translation (
         language_id char(2) not null,
         content_id  integer not null,
         body        text    not null,

         constraint pk_document_translation
             primary key(language_id, content_id),

         constraint fk_document_translation_content_translation
             foreign key(language_id, content_id) 
             references amnesia_translation.content_translation(language_id, content_id),

         constraint fk_document_translation_document
             foreign key(content_id) references document(content_id)
      );

#. Configure your application:

   .. code-block:: python

      def include_multilingual(config):
         config.include('amnesia_multilingual')
         config.include('amnesia_multilingual.modules.document')
         config.include('amnesia_multilingual.modules.folder')
         config.include('amnesia_multilingual.modules.event')
         config.include('amnesia_multilingual.modules.file')

      def main(global_config, **settings):
          config = Configurator(settings=settings, root_factory=some_root)
          config.include('amnesia')
          config.include(include_multilingual)
          config.commit()
