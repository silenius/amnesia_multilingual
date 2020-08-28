create schema if not exists amnesia_multilingual;

create table amnesia_multilingual.content_translation (
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
    on amnesia_multilingual.content_translation using gin(fts);

create table amnesia_multilingual.document_translation (
    language_id char(2) not null,
    content_id  integer not null,
    body        text    not null,

    constraint pk_document_translation
        primary key(language_id, content_id),

    constraint fk_document_translation_content_translation
        foreign key(language_id, content_id) 
        references amnesia_multilingual.content_translation(language_id, content_id),

    constraint fk_document_translation_document
        foreign key(content_id) references document(content_id)
);

create table amnesia_multilingual.event_translation (
    language_id char(2) not null,
    content_id  integer not null,
    body        text    not null,

    constraint pk_event_translation
        primary key(language_id, content_id),

    constraint fk_event_translation_content_translation
        foreign key(language_id, content_id) 
        references amnesia_multilingual.content_translation(language_id, content_id),

    constraint fk_event_translation_event
        foreign key(content_id) references event(content_id)
);

create table amnesia_multilingual.data_translation (
    language_id     char(2) not null,
    content_id      integer not null,
    mime_id         integer not null,
    original_name   text    not null,
    file_size       real    not null,
    path_name       serial  not null,

    constraint pk_data_translation
        primary key(language_id, content_id),

    constraint fk_data_translation_content_translation
        foreign key(language_id, content_id) 
        references amnesia_multilingual.content_translation(language_id, content_id),

    constraint fk_data_translation_data
        foreign key(content_id) references data(content_id),

    constraint fk_data_translation_mime
        foreign key(mime_id) references mime(id) deferrable initially deferred
);

insert into amnesia_multilingual.content_translation(language_id, content_id, title, description) 
select 'en', id as content_id, title, description from content;

alter table content drop column title;
alter table content drop column description;
alter table content drop column fts;

insert into amnesia_multilingual.document_translation select 'en', content_id, body from document;
alter table document drop column body;

insert into amnesia_multilingual.event_translation select 'en', content_id, body from event;
alter table event drop column body;

insert into amnesia_multilingual.data_translation select 'en', content_id, mime_id, original_name, file_size, path_name from data;
alter table data drop column original_name;
alter table data drop column file_size;
alter table data drop column path_name;
alter table data drop column mime_id;
