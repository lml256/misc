DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS student;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE student (
    name TEXT NOT NULL,
    id TEXT UNIQUE NOT NULL,
    chinese int NOT NULL,
    english int NOT NULL,
    math int NOT NULL,
    physical int NOT NUll
);
