CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    fname character varying(255),
    lname character varying(255),
    email character varying(255),
    ssn character varying(255),
    address character varying(255),
    cid character varying(255)
);

COPY students(id, fname, lname, email, ssn, address, cid)
FROM '/tmp/students.csv' DELIMITER '_' CSV HEADER;