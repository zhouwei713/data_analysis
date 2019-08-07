drop table if exists nvshen;
create table nvshen (
  id integer primary key autoincrement,
  name string not null,
  nvshen_id string not null
);

drop table if exists picture;
create table picture (
  id integer primary key autoincrement,
  nvshen_id string not null,
  pic_url string not null
);

drop table if exists score;
create table score (
  id integer primary key autoincrement,
  nvshen_id string not null,
  score string not null,
  userip string not null
);