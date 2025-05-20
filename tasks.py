import mysql.connector
from mysql.connector import Error
from datetime import datetime
import re

def remember():

    #Find Tasks Into the database
    connection = None
    try:
        connection = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="",
                                        database="jiya")
        print("Connection to MySQL DB successful")

        today = datetime.now().date()

        cursor = connection.cursor()
        query = "SELECT * FROM remember"  # Replace with your table name
        try:
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all records
            date = [row[1] for row in results]
                
        except Error as e:
            print(f"The error '{e}' occurred")
        
        for d in date:

            if today==d:

               tasks = [row[2] for row in results]
               return tasks
            else:
                return "No tasks are remaining"
        
    except Error as e:
        print(f"The error '{e}' occurred")

def p_d_tasks(data):

    #Find tasks from database
    connection = None
    try:
        connection = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="",
                                        database="jiya")
        print("Connection to MySQL DB successful")

        cursor = connection.cursor()
        query = "SELECT * FROM remember"  # Replace with your table name
        try:
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all records
            date = [row[1] for row in results]
        
            for d in date:
        
                if data==d:

                   tasks = [row[2] for row in results]
                   return tasks

                else:
                    return "Task Not Found"

        except Error as e:
            print(f"The error '{e}' occurred")
        
    except Error as e:
        print(f"The error '{e}' occurred")


def addtask(date,tasks):

    #Add Tasks into Base
    connection = None
    try:
        connection = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        password="",
                                        database="jiya")
        print("Connection to MySQL DB successful")

        cursor = connection.cursor()
        query = "INSERT INTO remember (date, tasks) VALUES (%s, %s)"
        values = (date, tasks)

        return "Work Done"

    except Error as e:
        print(f"The error '{e}' occurred")


        
