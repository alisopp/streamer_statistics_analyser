from mongoengine import *

db_client = connect('stream_reader', host='localhost', port=27017)

