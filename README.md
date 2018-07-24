# Flask-App
Python REST APIs with Flask, Docker, MongoDB, and AWS DevOps

## Flask Restful API
* A simple Flask Restful API using Flask-restful
* Make sure you have docker and docker-compose installed

## How to run
* Clone the repo
* $ cd Flask-App
* $ docker-compose build
* $ docker-compose up
* Open new terminal/cmd
* Find you docker machine IP by typing
* $ docker-machine ip
* Open your browser and type : http://your-docker-machine-ip:5000/
* if helloworld appears then its working fine
* Test API using POSTMAN

### Image Recognition with Inception-v3 (TensorFlow) Restful API
* Inception-v3 is trained for the ImageNet Large Visual Recognition Challenge using the data from 2012
* It can classify entire images upto 1000 different classes
* We can train our own model but right now I have used pre-trained Tensorflow models
* I have also modified classify_image.py to write top 5 output results into a file
  * for later reading and giving the results in POST request's response
* Read more details of the API in the release section
  * https://github.com/srafay/Flask-App/releases/tag/v0.3

### Similarity Check using Natural Language Processing Restful API
https://github.com/srafay/Flask-App/releases/tag/v0.2

### Database as a Service Restful API
https://github.com/srafay/Flask-App/releases/tag/v0.1
