#imports
import sqlite3

#create database
connection = sqlite3.connect('database.db')

#create schema of the database
with open('schema.sql') as f:
    connection.executescript(f.read())

#create cursor to execute queries
cur = connection.cursor()

#queries
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First post', 'Content of the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second post', 'Content of the second post')
            )

#confirm
connection.commit()

#close
connection.close()