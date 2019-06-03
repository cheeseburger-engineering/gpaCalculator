-- Create table
create table USER_ACCOUNT
(
USER_NAME VARCHAR2(30) not null,
SCHOOL    VARCHAR2(40) not null,
PASSWORD  VARCHAR2(30) not null,
primary key (USER_NAME)
);
 
-- Create table
create table GRADE
(
CODE  VARCHAR2(20) not null,
NAME  VARCHAR2(128) not null,
GPA FLOAT not null,
primary key (CODE)
) ;
 
-- Insert data: ---------------------------------------------------------------
 
insert into user_account (USER_NAME, SCHOOL, PASSWORD)
values ('channa', 'Drexel', 'cha001');
 
insert into user_account (USER_NAME, SCHOOL, PASSWORD)
values ('cam', 'Drexel', 'cam001');

insert into user_account (USER_NAME, SCHOOL, PASSWORD)
values ('matt', 'Drexel', 'mat001');

insert into user_account (USER_NAME, SCHOOL, PASSWORD)
values ('dan', 'Drexel', 'dan001');
 
insert into grade (CODE, NAME, GPA)
values ('4.0', 'Java Core', 3);
 
insert into grade (CODE, NAME, GPA)
values ('3.7', 'C# Core', 1);
 
-- Commit
Commit;