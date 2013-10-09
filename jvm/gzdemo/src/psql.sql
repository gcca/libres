create table md_user (
  user_name         varchar(15) not null primary key,
  user_pass         varchar(15) not null
);

create table md_user_role (
  user_name         varchar(15) not null,
  role_name         varchar(15) not null,
  primary key (user_name, role_name)
);

insert into md_user values ('gcca', '123');
insert into md_user_role values ('gcca', 'admin');
