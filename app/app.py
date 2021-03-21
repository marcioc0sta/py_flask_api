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

        hashedPw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": userName,
            "Password": hashedPw,
            "Sentence": "",
            "Tokens": 6
        })

        return jsonify({
            "status": 200,
            "msg": "You successfully signed up for the API"
        })


def verifyUser(username, password):
    hashedPw = users.find({'Username': username})[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashedPw) == hashedPw:
        return True
    else:
        return False


def countUserTokens(username):
    tokens = users.find({'Username': username})[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']
        sentence = postedData['sentence']

        correctPw = verifyUser(username, password)

        if not correctPw:
            return jsonify({
                "status": 302,
            })

        num_tokens = countUserTokens(username)

        if num_tokens <= 0:
            return jsonify({
                "status": 301,
            })

        users.update(
            {'Username': username},
            {"$set":  {
                "Sentence": sentence,
                "Tokens": num_tokens - 1
            }})

        return jsonify({
            "status": 201,
            "msg": "Sentence saved successfuly"
        })


class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData['username']
        password = postedData['password']

        correctPw = verifyUser(username, password)

        if not correctPw:
            return jsonify({
                "status": 302,
            })

        num_tokens = countUserTokens(username)

        if num_tokens <= 0:
            return jsonify({
                "status": 301,
            })

        sentence = users.find({'Username': username})[0]['Sentence']

        return jsonify({
            "status": 200,
            "sentence": sentence
        })


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

app.route('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
