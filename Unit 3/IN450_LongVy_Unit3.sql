/*
Unit 3 
Long Vy
*/

-- GeeksforGeeks. (2026, January 5). SQL: Creating roles. https://www.geeksforgeeks.org/sql/sql-creating-roles/ 

--Create security role
CREATE ROLE IN450a_security;
CREATE ROLE IN450b_security;
CREATE ROLE IN450c_security;


-- Grant SELECT to role for IN450a_security to all tables
GRANT SELECT ON IN450a to IN450a_security;
GRANT SELECT ON IN450b to IN450a_security;
GRANT SELECT ON IN450c to IN450a_security;

-- Grant Select to IN450b_security for IN450b table
GRANT SELECT ON IN450b to IN450b_security;

-- Grant Select to IN450c_security for IN450c table
GRANT SELECT ON IN450c to IN450c_security;


-- GeeksforGeeks. (2025, July 23). How to create login, user and grant permissions in SQL server. https://www.geeksforgeeks.org/sql-server/how-to-create-login-user-and-grant-permissions-in-sql-server/ 

--Create Login credentials
ALTER ROLE IN450a_security with LOGIN PASSWORD 'password1';
ALTER ROLE IN450b_security with LOGIN PASSWORD 'password2';
ALTER ROLE IN450c_security with LOGIN PASSWORD 'password3';






