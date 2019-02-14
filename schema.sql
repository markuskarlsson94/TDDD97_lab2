DROP TABLE IF EXISTS registred_users;

CREATE TABLE registred_users(name varchar(6) NOT NULL,
                             email varchar(30) NOT NULL,
                             password varchar(30) NOT NULL,
                             PRIMARY KEY(email));
