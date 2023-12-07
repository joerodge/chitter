DROP TABLE IF EXISTS peeps;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name text,
    username text,
    email text,
    password text
);

CREATE TABLE peeps (
    id SERIAL PRIMARY KEY,
    content text,
    time_stamp timestamp,
    user_id int,
    constraint fk_user foreign key(user_id)
        references users(id)
        on delete cascade
);

INSERT INTO users (name, username, email, password) VALUES ('Test name1', 'TestUsername1', 'test1@email.com', 'testpassword1');
INSERT INTO users (name, username, email, password) VALUES ('Test name2', 'TestUsername2', 'test2@email.com', 'testpassword2');

INSERT INTO peeps(content, time_stamp, user_id) VALUES ('Test peep1 from user 1', '2023-12-07 11:09:44.176188', 1);
INSERT INTO peeps(content, time_stamp, user_id) VALUES ('Test peep2 from user 1', '2023-12-07 11:32:29.716127', 1);
INSERT INTO peeps(content, time_stamp, user_id) VALUES ('Test peep1 from user 2', '2023-12-07 11:34:13.084608', 2);
INSERT INTO peeps(content, time_stamp, user_id) VALUES ('Test peep2 from user 2', '2023-12-07 11:44:34.612564', 2);

