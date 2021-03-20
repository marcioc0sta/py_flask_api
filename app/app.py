from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDB
users = db['Users']


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        userName = postedData['username']
        password = postedData['password']

        hashedPw = bcrypt.hashpw(password, bcrypt.gensalt())

        users.insert_one({
            "Username": userName,
            "Password": hashedPw,
            "Sentence": "",
            "Tokens": 6
        })

        return jsonify({
            "status": 200,
            "msg": "You successfully signed up for the API"
        })


api.add_resource(Register, '/register')

app.route('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
