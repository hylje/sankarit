CREATE TABLE player (
       id SERIAL primary key,
       username varchar(32) not null unique,
       email varchar(127) not null,
       password varchar(255) not null,
       gold integer not null
);

CREATE TABLE hero (
       id SERIAL primary key,
       name varchar(32) not null,
       class integer not null,
       xp integer not null,
       player_id integer not null references player (id) on delete cascade
);

CREATE TABLE adventure (
       id SERIAL primary key,
       start_time timestamp not null,
       end_time timestamp not null,
       class integer not null,
       gold integer not null
);

CREATE TABLE adventure_hero (
       adventure_id integer not null references adventure (id) on delete cascade,
       hero_id integer not null references hero (id),
       primary key (adventure_id, hero_id)
);

CREATE TABLE item (
       id SERIAL primary key,
       level integer not null,
       class integer not null,
       slot integer not null,
       rarity integer not null,
       player_id integer not null references player (id) on delete cascade,
       hero_id integer null references hero (id) on delete set null,
       adventure_id integer not null references adventure (id)
);
