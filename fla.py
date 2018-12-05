import json                       
import datetime 
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request,jsonify
from pymongo import MongoClient                    
from bson.objectid import ObjectId  
from passlib.hash import sha256_crypt

class JSONEncoder(json.JSONEncoder):                           
# extend json-encoder class
    def default(self, o):                               
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app= Flask(__name__)

# Config Mongo                                       
app.json_encoder = JSONEncoder
#app.secret_key = "#124122sadjh123"
mongo = MongoClient('localhost',27017)   
	
#Handle the requests

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/Signup', methods=['GET'])
def Signup():     
	return render_template('signup.html')

@app.route('/hsignup', methods=['POST'])
def hsignup():
	fname = request.form['fname']
	lname = request.form['lname']
	email = request.form['email']
	username = request.form['nickname']
	password = sha256_crypt.encrypt(str(request.form['pass']))
	secretq = request.form['secretq']
	secreta = request.form['secreta']

	# Jsonify data
	data = {'fname':fname, 'lname':lname, 'email':email,'username':username, 'password':password, 'sq':secretq, 'sa':secreta}

	# insert data
	mongo['capstone']['user'].insert_one(data)

	flash('You are now registered and can log in', 'success')
	return redirect(url_for('index.html'))   


# User login
"""@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
	# Get Form Fields
	username = request.form['username']
	password_candidate = request.form['password']

	# Create cursor
	cur = mysql.connection.cursor()

	# Get user by username
	result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

	if result > 0:
	    # Get stored hash
	    data = cur.fetchone()
	    password = data['password']

	    # Compare Passwords
	    if sha256_crypt.verify(password_candidate, password):
		# Passed
		session['logged_in'] = True
		session['username'] = username

		flash('You are now logged in', 'success')
		return redirect(url_for('home.html'))
	    else:
		error = 'Invalid login'
		return render_template('login.html', error=error)
	    # Close connection
	    cur.close()
	else:
	    error = 'Username not found'
	    return render_template('login.html', error=error)

   return render_template('login.html')"""

if __name__ == "__main__":
	app.run(debug=True)

