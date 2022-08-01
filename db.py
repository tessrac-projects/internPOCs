#from asyncio.windows_events import NULL
import flask
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt
app = flask.Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://ironman30:1234@cluster0.y2z9fjm.mongodb.net/database2?ssl=true&retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/users",methods=["GET"])
def home_page():
    Allusers = mongo.db.users.find()
    json_data = flask.jsonify(dumps(Allusers))
    return json_data

@app.route('/login',methods=['POST'])
def login():
    Email = request.json['Email']
    Password = request.json['password']
    
    bytePassword = Password.encode('utf-8')
    
    user = mongo.db.users.find_one({'Email':Email})
    hashed=user['password']
    if bcrypt.checkpw(bytePassword,hashed):
        return dumps(user)
    return 500

@app.route("/users/register",methods=['POST'])
def register():
    if request.method == 'POST' :
      existing_user = mongo.db.users.find_one({'Email':request.json['Email']})
      if existing_user is None: 
       Password = request.json['password']
       bytePassword = Password.encode('utf-8')
       salt = bcrypt.gensalt()
       hash = bcrypt.hashpw(bytePassword,salt)
       newUser = {'_id': ObjectId(),'firstname':request.json['firstname'],'middlename':request.json['middlename'],'lastname':request.json['lastname'],'Email':request.json['Email'],'phonenumber':request.json['phonenumber'],'address':request.json['address'],'password': hash}
       mongo.db.users.insert_one(newUser) 
       return dumps(newUser),201
      return {'status':0,'message':"username already existing"}
        
app.run()