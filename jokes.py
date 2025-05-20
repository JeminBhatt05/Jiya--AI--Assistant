import mysql.connector
from random import choice

# Function to create jokes table in the MySQL database if it doesn't exist
def create_jokes_table():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jokes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                joke TEXT NOT NULL
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"The error '{e}' occurred")


# Function to insert a joke into the MySQL database
def insert_joke(joke):
    try:
        create_jokes_table()
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        cursor = connection.cursor()
        query = "INSERT INTO jokes (joke) VALUES (%s)"
        cursor.execute(query, (joke,))
        connection.commit()
        cursor.close()
        connection.close()
        return "work done"
    except Error as e:
        print(f"The error '{e}' occurred")
        return "Error"

def get_random_joke():
    try:
        create_jokes_table()
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="jiya"
        )
        
        cursor = connection.cursor()
        
        # Fetch all jokes from the jokes table
        cursor.execute("SELECT joke FROM jokes")
        jokes = cursor.fetchall()  # Fetch all rows from the query
        
        if jokes:
            # Randomly select a joke from the list of jokes
            random_joke = choice(jokes)[0]  # jokes is a list of tuples, so we access the first element [0]
        else:
            random_joke = "No jokes available in the database."
        
        cursor.close()
        connection.close()
        
        return random_joke

    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
        return "Error fetching joke from the database."
