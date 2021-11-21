import os
import json
from flask.logging import default_handler
from flask import Flask
from pymongo import MongoClient
import pymongo
# import src.const as env_const
from src.config_api import FlaskApp

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        # if isinstance(o, ObjectId):
        #     return str(o)
        # if isinstance(o, datetime.datetime):
        #     return str(o)
        return json.JSONEncoder.default(self, o)


app = FlaskApp(__name__)
app.logger.removeHandler(default_handler)

try:
    # client = MongoClient('mongodb://{0}:{1}@{2}:27017/?authSource={3}'.format(env_const.MONGO_ADMIN_USER,env_const.MONGO_ADMIN_PWD,env_const.MONGO_HOSTNAME,env_const.MONGO_DATABASE),serverSelectionTimeoutMS=3000)
    client = MongoClient('mongodb://admin:admin@127.0.0.1:27017/?authSource=admin')
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as err:
    # do whatever you need
    print('Err:',err)
    
db =client.address_service

# use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONEncoder
# app.run(host='0.0.0.0', port=80, debug=True)