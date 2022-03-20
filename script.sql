

CREATE TABLE IF NOT EXISTS user (
        id integer PRIMARY KEY,
        user_id integer NOT NULL, 
        firstName text NOT NULL,
        lastName text NOT NULL,
        age text NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO user (user_id, firstName, lastName, age)
VALUES (1, "Khadija", "Lawal", "22");


