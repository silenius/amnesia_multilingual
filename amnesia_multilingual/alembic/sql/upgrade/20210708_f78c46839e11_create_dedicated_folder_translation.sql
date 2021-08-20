create schema if not exists amnesia_multilingual;

create table amnesia_multilingual.folder_translation (
    language_id char(2) not null,
    content_id  integer not null,

    constraint pk_folder_translation
        primary key(language_id, content_id),

    constraint fk_folder_translation_content_translation
        foreign key(language_id, content_id) 
        references amnesia_multilingual.content_translation(language_id, content_id),

    constraint fk_folder_translation_folder
        foreign key(content_id) references folder(content_id)
);

insert into amnesia_multilingual.folder_translation(language_id, content_id)
select language_id, content_id from amnesia_multilingual.content_translation
where amnesia_multilingual.content_translation.content_id in (
    select content_id from folder
);
