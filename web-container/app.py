"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"


        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens":6
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens

class Store(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3 verify the username pw match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)
        #Step 4 Verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        #Step 5 store the sentence, take one token away  and return 200OK
        users.update({
            "Username":username
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
        })

        retJson = {
            "status":200,
            "msg":"Sentence saved successfully"
        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        #Step 3 verify the username pw match
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status":302
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)

        #MAKE THE USER PAY!
        users.update({
            "Username":username
        }, {
            "$set":{
                "Tokens":num_tokens-1
                }
        })



        sentence = users.find({
            "Username": username
        })[0]["Sentence"]
        retJson = {
            "status":200,
            "sentence": str(sentence)
        }

        return jsonify(retJson)




api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__=="__main__":
    app.run(host='0.0.0.0')






"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient



app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
userNum = db["userNum"]
userNum.insert({
	"num_of_users":0
})

class Visit(Resource):
	def get(self):
		prev_num = userNum.find({})[0]["num_of_users"]
		new_num = prev_num + 1
		userNum.update({}, {"$set":{"num_of_users": new_num}})
		return ("Hello user:" + str(new_num))

def checkPostedData(postedData, functionName):
	if (functionName == "add" or functionName == "subtract" or functionName == "multiply" or functionName == "divide"):
		if "x" not in postedData or "y" not in postedData:
			return 301 # 301 according to API Resource chart means that some params are missing
		if functionName == "divide" and postedData["y"] == 0:
			return 302 # 302 according to API Resource chart means divide by zero error
		else:
			return 200
	else:
		return 601 # 601 according to API Resource chart means operation not supported

def performArithmaticOperation(x,y, functionName):
	if functionName == "add":
		return x+y
	if functionName == "subtract":
		return x-y
	if functionName == "multiply":
		return x*y
	if functionName == "divide":
		return x/y


class Arithmatic(Resource):
	def post(self):
		postedData = request.get_json()
		try:
			functionName = postedData["function"]
		except:
			return jsonify({"Message": "Error! no arithmatic operation specified"})
		statusCode = checkPostedData(postedData, functionName)
		if (statusCode != 200):
			return jsonify({
				"Message": "An error has occured!",	
				"Status Code": statusCode
				})
		x= postedData["x"]
		y= postedData["y"]
		result = performArithmaticOperation(x,y, functionName)
		retJSON = {
			"Message": result,
			"Status Code": 200
		}
		return jsonify(retJSON)

api.add_resource(Arithmatic, "/arithmatic")
api.add_resource(Visit, "/hello")


@app.route('/')
def hello_world():
	return "Hello World"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
"""