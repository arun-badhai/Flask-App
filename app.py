from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
	return "Hello World"

@app.route('/add', methods=["POST"])
def addNums():
	dataDict = request.get_json()
	if "x" not in dataDict or "y" not in dataDict:
		return "Error, incomplete arguments!", 305
	x = dataDict["x"]
	y = dataDict["y"]
	z = x+y
	retJSON = {
		"result": z
	}
	return jsonify(retJSON)

if __name__ == "__main__":
	app.run(debug=True)
