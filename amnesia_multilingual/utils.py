from operator import attrgetter

from sqlalchemy import inspect
from sqlalchemy import sql
from sqlalchemy import orm

from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

from amnesia.utils.locale import get_current_locale
from amnesia.utils.locale import get_default_locale
from amnesia.utils.locale import get_locales
from amnesia_multilingual.modules.content import ContentTranslation


def with_translation_criteria(request=None, include_aliases=True):
    current_locale, default_locale = get_locales(request)

    criteria = orm.with_loader_criteria(
        ContentTranslation,
        lambda cls: cls.language_id.in_(
            (current_locale, default_locale)
        ),
        include_aliases=include_aliases
    )

    return criteria

#def with_translations(stmt, entity, request=None):
#    if request is None:
#        registry = get_current_registry()
#    else:
#        registry = request.registry
#
#    insp = inspect(entity)
#    base = insp.class_
#    options = [with_translation_criteria(request)]
#    join = None
#    translations = registry['amnesia.translations']['mappings']
#
#    if insp.is_aliased_class:
#        content_cls = {_.class_ for _ in insp.with_polymorphic_mappers}
#        aliased = [t for c, t in translations.items() if c in content_cls]
#
#        join = entity.translations.of_type(
#            orm.with_polymorphic(ContentTranslation, aliased)
#        )
#
#        options = (
#            orm.contains_eager(
#                getattr(getattr(entity, cls.__name__), 'translations')
#            )
#            for cls in content_cls if cls is not base
#        )
#    elif insp.is_mapper:
#        join = entity.translations
#
#        options.append(
#            orm.contains_eager(entity.translations)
#        )
#
#    if join:
#        stmt = stmt.join(join)
#
#    stmt = stmt.options(
#        orm.contains_eager(entity.translations),
#        *options
#    )
#
#    return stmt

def with_current_translations(stmt, entity, request=None, innerjoin=True):
    if request is None:
        registry = get_current_registry()
    else:
        registry = request.registry

    insp = inspect(entity)
    base = insp.base_mapper.class_
    current_locale, default_locale = get_locales(request)
    translations = registry['amnesia.translations']['mappings']
    stmt_join = stmt.join if innerjoin else stmt.outerjoin

    # orm.with_polymorphic entity
    if insp.is_aliased_class:
        content_cls = {_.class_ for _ in insp.with_polymorphic_mappers}

        # Mappings from Content-like classes to corresponding
        # ContentTranslation-like classes
        aliased = [t for c, t in translations.items() if c in content_cls]

        translation_cls = orm.with_polymorphic(ContentTranslation, aliased)

        partition = sql.select(
            translation_cls,
            sql.func.row_number().over(
                order_by=[
                    sql.desc(translation_cls.language_id == current_locale),
                    sql.desc(translation_cls.language_id == default_locale)
                ],
                partition_by=translation_cls.content_id
            ).label('index')
        ).where(
            translation_cls.language_id.in_((current_locale, default_locale))
        ).subquery()

        partition_alias = orm.aliased(
            translation_cls, partition, flat=True
        )

        options = (
            orm.contains_eager(
                getattr(getattr(entity, cls.__name__), 'current_translation'),
                alias=partition
            )
            for cls in content_cls if cls is not base
        )

        stmt = stmt_join(
            partition_alias,
            sql.and_(
                partition_alias.content_id==entity.id,
                partition.c.index==1
            )
        ).options(
            #orm.contains_eager(entity.current_translation.of_type(partition_alias))
            orm.contains_eager(entity.current_translation, alias=partition),
            *options
        )

        return (stmt, partition)
    elif insp.is_mapper:
        stmt = stmt_join(
            entity.current_translation
        ).options(
            orm.contains_eager(
                entity.current_translation,
                alias=entity._current_translation_partition
            )
        )

        if insp.class_ is not base:
            stmt = stmt.options(
                orm.contains_eager(
                    entity.content_current_translation,
                    alias=entity._current_translation_partition
                )
            )

        return (stmt, entity._current_translation_partition)
