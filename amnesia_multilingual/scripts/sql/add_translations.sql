create schema if not exists amnesia_translation;

create table amnesia_translation.content_translation (
    language_id char(2)     not null,
    content_id  integer     not null,
    title       mediumtext  not null,
    description text,
    fts         tsvector,

    constraint pk_content_translation
        primary key(language_id, content_id),

    constraint fk_content_translation_language
        foreign key(language_id) references language(id),

    constraint fk_content_translation_content
        foreign key(content_id) references content(id)
);

create index idx_content_translation_fts
    on amnesia_translation.content_translation using gin(fts);

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

create table amnesia_translation.event_translation (
    language_id char(2) not null,
    content_id  integer not null,
    body        text    not null,

    constraint pk_event_translation
        primary key(language_id, content_id),

    constraint fk_event_translation_content_translation
        foreign key(language_id, content_id) 
        references amnesia_translation.content_translation(language_id, content_id),

    constraint fk_event_translation_event
        foreign key(content_id) references event(content_id)
);

insert into amnesia_translation.content_translation(language_id, content_id, title, description) 
select 'en', id as content_id, title, description from content;

alter table content drop column title;
alter table content drop column description;
alter table content drop column fts;

insert into amnesia_translation.document_translation select 'en', content_id, body from document;
alter table document drop column body;

insert into amnesia_translation.event_translation select 'en', content_id, body from event;
alter table event drop column body;
