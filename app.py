'''
Anton Kanugalwattage
July 4, 2019
Amazon Price Watch application
'''

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient
from popularSubjectGetter import popularSubjectGetter
from popularCoursesGetter import popularCoursesGetter
from newRating import newRating
from sendEMail import sendEMail
from latestSubjectGetter import latestSubjectGetter 

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h3>Welcome to backend of Price Watch</h3><h4>By Anton Kanugalawattage</h4>"

# @app.route('/products')
# def products():
#     # cluster = MongoClient("")
#     # db = cluster['PriceWatch']
#     # collection = db['PriceWatch-Products']
#     # content = list(collection.find())
#     # return jsonify(content)
#     return ""

@app.route('/getTutor')
def getTutor():
    cluster = MongoClient("mongodb+srv://tUser:sUqOIWMnEz5a8sqn@tutorfy-ednqp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['Tutorfy']
    collection = db['Tutorfy']
    content = list(collection.find())
    return jsonify(content)

@app.route('/addTutor', methods = ['POST'])
def addTutor():
    tutor = request.get_json()
    cluster = MongoClient("mongodb+srv://tUser:sUqOIWMnEz5a8sqn@tutorfy-ednqp.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['Tutorfy']
    collection = db['Tutorfy']
    print(tutor['name'])
    jsonfile = {
        "_id": int(list(collection.find())[-1]['_id'])+1,
        "name": tutor['name'],
        "courseName": tutor["courseName"],
        "subject": tutor["subject"],
        "courseCode": tutor["courseCode"],
        "credentials": tutor["credentials"],
        "description": tutor["description"],
        "image": tutor["image"],
        "university": tutor["university"],
        "rating": float(tutor["rating"]),
        "numberOfRatings": int(tutor["numberOfRatings"]),
        "email": tutor["email"],
        "phone": tutor["phone"],
        "price": float(tutor["price"])
	        }
    collection.insert_one(jsonfile)
    return "tutor_added"

#update rating
@app.route('/updateRating', methods = ['POST'])
def updateRating():
    data = request.get_json()
    return newRating(data['_id'], data['rating'])

#popular subjects
@app.route('/getPopularSubjects')
def getPopularSubjects():
    return popularSubjectGetter()

#popular subjects
@app.route('/getPopularCourses')
def getPopularCourses():
    return popularCoursesGetter()

@app.route('/getLatestSubjects')
def getLatestSubjects():
    return latestSubjectGetter()


@app.route('/contactTutor', methods = ['POST'])
def contactTutor():
    data = request.get_json()
    return sendEMail(data['tutorEmail'], data['message'], data['email'])


#popular courses

#new courses


# @app.route('/addProduct', methods = ['POST'])
# def addProduct():
#     # productData = request.get_json()
#     # return newProduct(productData['title'], productData['email'])
#     return ""


# @app.route('/rmProduct', methods = ['POST'])
# def rmProduct():
#     # productData = request.get_json()
#     # return removeProduct(int(productData['id']), productData['email'])
#     return ""

# @app.route('/priceCheck')
# def priceCheck():
#     # return priceChecker()
#     return ""

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run()