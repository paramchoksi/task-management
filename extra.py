import mysql.connector
# from mysql.connector import Error
from Database import *
from datetime import datetime


username = 'deep patel'
email = 'deeppatel@gmail.com'
password = 'Param%2000'
table_name = 'newparamchoksi'
title = 'Clean Rooms'
desc = 'Before Tonight'
sno = 3

delete_query = "DELETE FROM {0} WHERE sno = {1}".format(table_name, sno)
executeQuery(createDatabaseConnection(), delete_query)
print("Your row is successfully deleted")


executeQuery(createDatabaseConnection(), "ALTER TABLE {} DROP sno".format(table_name))
executeQuery(createDatabaseConnection(), "ALTER TABLE {} AUTO_INCREMENT = 1".format(table_name))
executeQuery(createDatabaseConnection(), "ALTER TABLE {} ADD sno int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST".format(table_name))
