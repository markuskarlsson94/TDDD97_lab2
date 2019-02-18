DROP TABLE IF EXISTS registered_users;
DROP TABLE IF EXISTS logged_in_users;

CREATE TABLE registered_users(name varchar(30) NOT NULL,
                             email varchar(30) NOT NULL,
                             password varchar(30) NOT NULL,
                             PRIMARY KEY(email));

CREATE TABLE logged_in_users(email varchar(30) NOT NULL,
                             token varchar(36) NOT NULL,
                             PRIMARY KEY(token));
