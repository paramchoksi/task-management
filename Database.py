import mysql.connector
from mysql.connector import Error
import pandas as pd


def createServerConnection():
    """
    This function create a connection with the mySQL server
    """
    server_connection = None
    try:
        server_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='param%2000'
        )
        print("MySql Server Connection Successful")
    except Error as err:
        print(f"Error: '{err}'")
    return server_connection


def createDatabaseConnection():
    """
    This function create a conncetion with mention database in mysql server
    """
    database_connection = None
    try:
        database_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='param%2000',
            database='todo'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return database_connection


def executeQuery(database_connection, query):
    cursor = database_connection.cursor()
    try:
        cursor.execute(query)
        database_connection.commit()
        print("Query Execute successfully")
        return True
    except Error as err:
        print(f"Error: '{err}'")


def checkDatabaseConnection():
    try:
        connection = None
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='param%2000',
            database='todo'
        )
        return True
    except:
        return False

# def createDatabase(server_connection, query):
#     """
#     This function create a database in mysql server
#     """
#     cursor = server_connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Database Created Successful")
#     except Error as err:
#         print(f"Error: '{err}'")


# def dropDatabase(db_name):
#     try:
#         drop_db_query = "DROP DATABASE {}".format(db_name)
#         executeQuery(createDatabaseConnection(), drop_db_query)
#         print("{} Table droped successfully")
#     except Error as err:
#         print(f"Error: '{err}'")


def createLoginTable():
    try:
        login_table_query = """
        CREATE TABLE LOGIN (
            username VARCHAR(30),
            email VARCHAR(30) PRIMARY KEY,
            passwd VARCHAR(30) UNIQUE
        )
        """
        if executeQuery(createDatabaseConnection(), login_table_query):
            print("Login Table is created Successfully")
    except Error as err:
        print(f"Error: '{err}'")


def createUserTodoTable(table_name):
    try:
        user_table_query = """
        CREATE TABLE {0} (
            sno INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200),
            description VARCHAR(500),
            time TIMESTAMP
        )
        """.format(table_name)
        if executeQuery(createDatabaseConnection(), user_table_query):
            print("{0} Table is successfully created".format(table_name))
    except Error as err:
        print(f"Error: '{err}'")


def getDataFromTable(database_connection, column_name, table_name):
    cursor = database_connection.cursor()
    try:
        cursor.execute("SELECT {} from {}".format(column_name, table_name))
        Data = cursor.fetchall()
        print("{0} data from {1} table is got successfully".format(column_name, table_name))
        return Data
    except Error as err:
        print(f"Error: '{err}'")


def getAllDataFromTable(table_name):
    try:
        select_query = """
            SELECT * FROM {0}
        """.format(table_name)
        return executeQuery(createDatabaseConnection(), select_query)
    except Error as err:
        print(f"Error: '{err}'")


def getAllTables(database_connection):
    cursor = database_connection.cursor()
    try:
        cursor.execute("SHOW TABLES")
        Tables = cursor.fetchall()
        print("All tables fetched successfully from database..!!")
        return Tables
    except Error as err:
        print(f"Error: '{err}'")


def updateUserTodo(database_connection, table_name, title, desc, time, todo_no):
    cursor = database_connection.cursor()
    try:
        cursor.execute("""
        UPDATE {0} 
        SET
          title = "{1}", 
          description = "{2}",
          time = "{3}"
        WHERE 
          sno = {4}
        """.format(table_name, title, desc, time, todo_no))
        database_connection.commit()
        print("Your todo is Updated")
        return True
    except Error as err:
        print(f"Error: '{err}'")


def getUserTodo(database_connection, table_name, sno):
    cursor = database_connection.cursor()
    try:
        cursor.execute("""
        SELECT title, description FROM {0} WHERE sno = {1}
        """.format(table_name, sno))
        todo = cursor.fetchall()
        print("Your todo is fetched successfully")
        return todo
    except Error as err:
        print(f"Error: '{err}'")


createLoginTable()

