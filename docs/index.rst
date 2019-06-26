.. _index:

===========================
Amnesia multilingual plugin
===========================

Amnesia multilingual content plugin provides multi-language support for
Content-based content types in AmnesiaCMS.

=====
Usage
=====

#. Install package:

   .. code-block:: bash

      pip install amnesia_multilingual


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
