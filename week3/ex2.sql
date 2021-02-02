-- dmitrii polushin
-- timur nugaev
-- kamil agliullin

CREATE TABLE movies (
    title VARCHAR PRIMARY KEY,
    year INT PRIMARY KEY,
    plot VARCHAR,
    length INT
);

CREATE TABLE genres (
    id INT PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE directors (
    name VARCHAR PRIMARY KEY,
    dob INT PRIMARY KEY
);

CREATE TABLE actors (
    name VARCHAR PRIMARY KEY,
    bod INT PRIMARY KEY
);

CREATE TABLE company (
    name VARCHAR PRIMARY KEY,
    address VARCHAR
);

CREATE TABLE direct_by (
    m_name VARCHAR FOREIGN KEY REFERENCES movies(title, year),
    director VARCHAR FOREIGN KEY REFERENCES directors(name, dob)
);

CREATE TABLE starred_in (
    a_name VARCHAR FOREIGN KEY REFERENCES actor(name, dob),
    m_name VARCHAR FOREIGN KEY REFERENCES movies(title, year)
);

CREATE TABLE have_genres (
    genre VARCHAR FOREIGN KEY REFERENCES genres(id),
    movie VARCHAR FOREIGN KEY REFERENCES movies(title, year)
);

CREATE TABLE qq (
    actor VARCHAR FOREIGN KEY REFERENCES actors(name, dob),
    monie VARCHAR FOREIGN KEY REFERENCES movies(title, year),
    quote VARCHAR
);

CREATE TABLE produced_by (
    company VARCHAR FOREIGN KEY REFERENCES company(name),
    movie VARCHAR FOREIGN KEY REFERENCES movies(title, year)
);