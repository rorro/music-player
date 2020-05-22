drop table if exists songs;
drop table if exists user_votes;

CREATE TABLE if not exists songs (
    link varchar(300) PRIMARY KEY,
    upvotes integer,
    downvotes integer
);

CREATE TABLE if not exists user_votes (
    id integer PRIMARY KEY AUTOINCREMENT,
    token varchar(36),
    link varchar(300),
    vote integer,
    UNIQUE(token, link)
);

pragma foreign_keys = on
