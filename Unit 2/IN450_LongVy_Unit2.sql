--Create IN450A Table

CREATE TABLE IN450A(
	"Time" TEXT,
	Source CHAR(30),
	Destination CHAR(30),
	Protocol CHAR(30),
	Length TEXT
);

--Copy data into IN450A table

COPY in450a FROM '/Users/titanstower/Documents/School Work/IN450/Student Files/IN450A.csv'
DELIMITER ',' CSV HEADER;

Select * from IN450a;





--Create IN450B Table

CREATE TABLE IN450B(
	first_name CHAR(50),
	last_name CHAR(50),
	email CHAR(50),
	Source CHAR(50),
	Destination CHAR(30)
);


--Copy data into IN450B table

COPY in450b(first_name, last_name, email, Source, Destination)
FROM '/Users/titanstower/Documents/School Work/IN450/Student Files/IN450B.csv'
DELIMITER ',' CSV HEADER;

Select * from IN450b;



--Create IN450C Table

CREATE TABLE IN450C(
	AppID CHAR(50),
	AppName CHAR(50),
	AppVersion CHAR(10),
	Source CHAR(50),
	Destination CHAR(50),
	DigSig CHAR(500)
);

--Copy data into IN450C table

COPY in450c(AppID, AppName, AppVersion, Source, Destination, DigSig)
FROM '/Users/titanstower/Documents/School Work/IN450/Student Files/IN450C.csv'
DELIMITER ',' CSV HEADER;

Select * from IN450C

