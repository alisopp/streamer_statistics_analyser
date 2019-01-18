# test file to test if the docker sets its env variables right
import os

db_port = os.environ['DB_PORT']
db_host = os.environ['DB_HOST']

print (db_port)
print (db_host)

file = open("hello.txt", "a")

file.write(db_host)
