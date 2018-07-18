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
