CREATE DATABASE hackhaton;

USE hackhaton;

CREATE TABLE "user" (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20) NOT NULL
);

CREATE TABLE office (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude numeric,
    longitude numeric,
);

CREATE TABLE route (
    id UUID PRIMARY KEY,
    directions_text TEXT NOT NULL,
    latitude numeric,
    longitude numeric,
    office_id UUID NOT NULL,
    owner_id UUID NOT NULL,
    FOREIGN KEY (office_id) REFERENCES office(id),
    FOREIGN KEY (owner_id) REFERENCES "user"(id)
);

CREATE TABLE driver_route (
    id UUID PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    max_capacity INT NOT NULL,
    passenger_count INT DEFAULT 0,
    route_id UUID,
    FOREIGN KEY (route_id) REFERENCES route(id)
);


CREATE TABLE passenger_route (
    id UUID PRIMARY KEY,
    date_from DATE,
    date_to DATE,
    max_distance FLOAT,
    route_id UUID,
    FOREIGN KEY (route_id) REFERENCES route(id)
);

CREATE TABLE "match" (
    id UUID PRIMARY KEY,
    passenger_route_id UUID NOT NULL,
    driver_route_id UUID NOT NULL,
    FOREIGN KEY (driver_route_id) REFERENCES driver_route(id),
    FOREIGN KEY (passenger_route_id) REFERENCES passenger_route(id)
);

DROP TABLE "match" CASCADE;
DROP TABLE passenger_route CASCADE;
DROP TABLE driver_route CASCADE;
DROP TABLE route CASCADE;
DROP TABLE office CASCADE;
DROP TABLE "user" CASCADE;

SELECT * 
FROM matches;