DROP TABLE IF EXISTS registered_users;
DROP TABLE IF EXISTS logged_in_users;
DROP TABLE IF EXISTS messages;

CREATE TABLE registered_users(name varchar(30) NOT NULL,
                             email varchar(30) NOT NULL,
                             password varchar(30) NOT NULL,
                             PRIMARY KEY(email));

CREATE TABLE messages(email varchar(30) NOT NULL,
                      sender varchar(30) NOT NULL,
                      message varchar(400) NOT NULL,
                      FOREIGN KEY(email) REFERENCES registered_users(email)
                      FOREIGN KEY(sender) REFERENCES registered_users(email));

CREATE TABLE logged_in_users(email varchar(30) NOT NULL,
                             token varchar(36) NOT NULL,
                             PRIMARY KEY(token));

INSERT INTO registered_users VALUES("fisk", "fisk@mail.com", "aaaaaaaa");
INSERT INTO messages VALUES("fisk@mail.com", "fisk@mail.com", "hej fisk");
INSERT INTO messages VALUES("fisk@mail.com", "fisk@mail.com", "hej då fisk");
