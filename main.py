from flask import Flask, request, Response
from firebase import firebase
import os
import random
import json
import pyodbc


app = Flask(__name__)


server = os.getenv('SERVER')
database = 'votingDB'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
driver= '{ODBC Driver 17 for SQL Server}'


with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM CARD")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()