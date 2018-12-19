import json                       
import datetime 
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request,jsonify
from flask import Markup
from pymongo import MongoClient                    
from bson.objectid import ObjectId  
from passlib.hash import sha256_crypt

# App config
app= Flask(__name__)                                
app.secret_key = "testkey"
app.config['SESSION_TYPE'] = 'filesystem'
mongo = MongoClient('localhost',27017)   
	
#Handle the requests

@app.route('/')
def index():
	if session['logged_in']:
		return redirect('/home')
	else:
		return render_template('index.html')

@app.route('/Signup', methods=['GET'])
def Signup():     
	return render_template('signup.html')

@app.route('/hsignup', methods=['POST'])
def hsignup():
	fname = request.form['fname']
	lname = request.form['lname']
	email = request.form['email']
	#username = request.form['nickname']
	password = sha256_crypt.encrypt(str(request.form['pass']))
	secretq = request.form['secretq']
	secreta = request.form['secreta']

	# Jsonify data
	data = {'fname':fname, 'lname':lname, 'email':email, 'password':password, 'sq':secretq, 'sa':secreta}

	# insert data
	mongo['capstone']['user'].insert_one(data)
	flash('You are now registered and can log in','Success')
	return redirect('/')   


# User login
@app.route('/login', methods=['POST'])
def login():
   if request.method == 'POST':
	# Get Form Fields
	email = request.form['email']
	password_candidate = request.form['pass']

 	#Query for user name
	result = mongo['capstone']['user'].find_one({'email':email})
	

	if result is None:

		flash('Invalid UserName or Password','Oops!')
		return redirect('/')   

	else:

	    # Get stored hash
	    password = result['password']

	    # Compare Passwords
	    if sha256_crypt.verify(password_candidate, password):
		# Passed
			session['logged_in'] = True
			session['username'] = result['fname']

			return redirect('/home')
	    
	    else:
		
			flash('Invalid UserName or Password','Oops!')
			return redirect('/')   



@app.route('/home', methods=['GET'])
def home():
	if session['logged_in']:
		content = getContentHome()
		return render_template('home.html',user_name='Hi! '+session['username'],content=content)
	else:
		flash('Please login to continue','Oops!')
		return redirect('/')  		

@app.route('/logout')
def logout():
	if session['logged_in']:
		session['logged_in'] = False
		session['username']  = ''
		flash('You have been logged out','Success!')
		return redirect('/')   
	else:
		flash('You have been logged out','Success!')
		return redirect('/')

@app.route('/predict')
def predictor():
	if session['logged_in']:
		content = getContentPredict()
		return render_template('home.html',user_name='Hi! '+session['username'],content=content)
	else:
		flash('Please login to continue','Oops!')
		return redirect('/') 


#Home Content returned Here 
def getContentHome():
	welx = open('templates/welx.html','r').read()
	return Markup(welx)

#Predict Content returned Here 
def getContentPredict():
	pred = open('templates/form.html','r').read()
	return Markup(pred)

if __name__ == "__main__":
	app.run(debug=True)

