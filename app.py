from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
	if (functionName == "add"):
			if "x" not in postedData or "y" not in postedData:
				return 301
				# 301 according to API Resource chart means that some params are missing
			else:
				return 200

class Add(Resource):
	def post(self):
		postedData = request.get_json()
		statusCode = checkPostedData(postedData, "add")
		if (statusCode != 200):
			return ({
				"Message": "An error has occured!",	
				"Status Code": statusCode
			})
		x= postedData["x"]
		y= postedData["y"]
		result = int(x) + int(y)
		retJSON = {
			"Message": result,
			"Status Code": 200
		}
		return jsonify(retJSON)

class Subtract(Resource):
	def post(self):
		pass

class Multiply(Resource):
	def post(self):
		pass

class Divide(Resource):
	def post(self):
		pass

api.add_resource(Add, "/add")


@app.route('/')
def hello_world():
	return "Hello World"

if __name__ == "__main__":
	app.run(debug=True)
