# Long Vy
# Presentation layer
# Unit 2



"""
References
GeeksforGeeks. (2022, December 2). Introduction to psycopg2 module in python. https://www.geeksforgeeks.org/python/introduction-to-psycopg2-module-in-python/ 
Luna, J. C. (2025, March 21). Managing postgresql databases in python with psycopg2 | datacamp. DataCamp. https://www.datacamp.com/tutorial/tutorial-postgresql-python 
"""


import psycopg2

class Business_Layer:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres"
        )
        self.cursor = self.connection.cursor()

    def get_row_count_450a(self):
        self.cursor.execute("SELECT COUNT(*) FROM in450a")
        result = self.cursor.fetchone()
        return result[0]
    
    def get_450b(self):
        self.cursor.execute("SELECT first_name, last_name FROM in450b")
        result = self.cursor.fetchall()
        return result
    
    def close_connection(self):
        self.cursor.close()
        self.connection.close()