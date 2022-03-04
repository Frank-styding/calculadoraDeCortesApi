from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)


























class Users(Resource):
    
    def post(self): # convert dataframe to dictionary
        print(request.get_json())
        return request.get_json(), 200
    
    def get(self):
        print(request.get_json())
        return {'data':"hola"}
    
class Locations(Resource):
    # methods go here
    pass
    
api.add_resource(Users, '/users')  # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations

if __name__ == '__main__':
    app.run() 