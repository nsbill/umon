# USER MONITORING
Aleksandr Kirilyuk alx@nsbill.ru

https://github.com/docker-library/postgres.git


1. cd app/db/postgresql
2. docker build -t postgresql10.1/alpine .

# Создание базы данных и пользователя в PGSQL
```
postgres=# create database dbumon;
CREATE DATABASE
postgres=# create user dbuser with password 'dbpassword';
CREATE ROLE
postgres=# grant ALL on DATABASE dbumon to dbuser;
GRANT
```           
