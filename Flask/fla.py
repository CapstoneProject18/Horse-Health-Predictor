from __future__ import print_function
import sys
import datetime 
import numpy as np
import pandas as pd 
from flask import Flask
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import logging
from flask import request
from flask import Markup
from pymongo import MongoClient                    
from bson.objectid import ObjectId  
from passlib.hash import sha256_crypt
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.externals import joblib


# App config
app= Flask(__name__)                                
app.secret_key = "testkey"
app.config['SESSION_TYPE'] = 'filesystem'
mongo = MongoClient('localhost',27017)   
	
#Handle the requests
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/signup', methods=['GET'])
def signup():     
	return render_template('signup.html')

@app.route('/hsignup', methods=['POST'])
def hsignup():
	fname = request.form['fname']
	lname = request.form['lname']
	email = request.form['email']
	password = sha256_crypt.encrypt(str(request.form['pass']))
	secretq = request.form['secretq']
	secreta = request.form['secreta']
	# Create Data Dict
	data = {'fname':fname, 'lname':lname, 'email':email, 'password':password, 'sq':secretq, 'sa':secreta}
	# insert data
	result = mongo['capstone']['user'].find_one({'email':email})
	if result is None:
		mongo['capstone']['user'].insert_one(data)
		flash('You are now registered and can log in','Success')
		return redirect('/')
	else:
		flash('You are already registered! Please login','Oops!')
		return redirect('/')  

@app.route('/fpassword')
def fpassword():
	return render_template('fp.html')

@app.route('/findaccount',methods=['POST'])
def findaccount():
	if request.method == 'POST':
		email = request.form['email']
		result = mongo['capstone']['user'].find_one({'email':email})
		session['em'] = result['email']
		if result is None:
			flash('Invalid UserName ')
			return redirect('/') 
		else:
			return render_template('answer.html',secretq=result['sq'],)

@app.route('/answer',methods=['POST'])
def answer():
	secreta_candidate = request.form['secreta']
	email=session['em']
	result = mongo['capstone']['user'].find_one({'email':email})
	secreta = result['sa']
	if secreta_candidate == secreta:
		return render_template('cpassword.html')
	else:
		session['em']=''
		flash('Wrong answer, please retry')
		return redirect('/answer')

@app.route('/cpassword',methods=['POST'])
def cpassword():
	email=session['em']
	result = mongo['capstone']['user'].find_one({'email':email})
	result['password'] = sha256_crypt.encrypt(str(request.form['password']))
	mongo['capstone']['user'].update_one({'email':email},{'$set':result},upsert=False)
	session['em']=''
	flash('Your Password has been changed successfully','Success!')
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
			session['email'] = result['email']
			return redirect('/home')	    
	    else:		
			flash('Invalid UserName or Password','Oops!')
			return redirect('/')   



@app.route('/home')
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
		session['email'] = ''
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

@app.route('/stats')
def stats():
	if session['logged_in']:
		content = getContentStats()
		return render_template('home.html',user_name='Hi! '+session['username'],content=content)
	else:
		flash('Please login to continue','Oops!')
		return redirect('/')

@app.route('/hpredict',methods=['POST'])
def hpredict():
	df = pd.read_csv('out.csv')
	df.drop(df.columns[0], axis=1,inplace=True)
	#get parametres from form and make data frames
	fin = {'temp_of_extremities':request.form['TempExt'],
				'peripheral_pulse':request.form['perpulse'],
				'mucous_membrane':request.form['mucmem'],
				'capillary_refill_time':request.form['capref'],
				'pain':request.form['pain'],
				'peristalsis':request.form['pstals'],
				'abdominal_distention':request.form['abdist'],
				'nasogastric_tube':request.form['nstube'],
				'nasogastric_reflux':request.form['nsreflux'],
				'rectal_exam_feces':request.form['recexam'],
				'abdomen':request.form['abd'],
				'surgical_lesion':request.form['slesion'],
				'age':request.form['age'],
				'surgery':request.form['surgery'],
				'rectal_temp':request.form['rtemp'],
				'pulse':request.form['pulse'],
				'respiratory_rate':request.form['resprate'],
				'packed_cell_volume':request.form['pcv'],
				'total_protein':request.form['tprotein'],
				'outcome':'lived'
				}
	#Convert to the required form
	fin = pd.DataFrame(fin,index=[299])
	df=df.append(fin)
	print(df, file=sys.stdout)
	cat_df = df.select_dtypes(include=['object'])
	df.drop(['temp_of_extremities','peripheral_pulse',
			 'mucous_membrane', 'capillary_refill_time',
			 'pain','peristalsis', 'abdominal_distention',
			 'nasogastric_tube','nasogastric_reflux',
			 'rectal_exam_feces', 'abdomen','outcome',
			 'surgery','surgical_lesion','age'],axis=1,inplace=True)
	min_max_scaler = preprocessing.MinMaxScaler()
	df = pd.DataFrame(min_max_scaler.fit_transform(df))
	cat_df = pd.get_dummies(cat_df,columns=['temp_of_extremities',
			'peripheral_pulse', 'mucous_membrane',
			'capillary_refill_time', 'pain','peristalsis',
			'abdominal_distention', 'nasogastric_tube',
       		'nasogastric_reflux', 'rectal_exam_feces',
       		'abdomen','surgery','surgical_lesion','age'])
	le = LabelEncoder()
	le.fit(["died","euthanized","lived"])
	cat_df['outcome'] = le.transform(cat_df['outcome'])
	findata = pd.DataFrame(data=pd.concat([cat_df,df],axis=1))
	#Train model and predict, joblib causing fatal errors
	x = findata[findata.index!=299].drop('outcome',axis=1).values
	y = findata[findata.index!=299]['outcome'].values
	model = RandomForestClassifier(n_estimators=100)
	model.fit(x,y)
	pred = model.predict(findata[findata.index==299].drop('outcome',axis=1))
	#Convert to Text
	if pred==[1]:
		pred="Likely to be euthanized :("
	elif pred==[2]:
		pred="Likely to die :("
	else:
		pred="Likely to live :)"
	#Save to mongo and redirect to history!	
	mongo['capstone']['history'].insert_one({'user':session['email'],
	'pred':pred,'time':datetime.datetime.now(), 'Hname':request.form['hname']})
	return redirect('/history')

@app.route('/history')
def history():
		if session['logged_in']:
			content = getContentHistory()
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

#Stats content returned here
def getContentStats():
	stats = open('templates/graph.html','r').read()
	return Markup(stats)

def getContentHistory():
	hist=''
	cursor = mongo['capstone']['history'].find({'user':session['email']})
	for document in cursor:
		hist+= '<div class="row">'
		hist+= '<div class="col-lg-12 text-center">'
		hist+= '<h1 class="mt-5">'
		hist+= document['Hname']
		hist+= '</h1>'
		hist+= '<p class="lead">'
		hist+= document['pred']
		hist+= '</p>'
		hist+= '<ul class="list-unstyled">'
		hist+= '<li>'
		hist+= document['time'].strftime("%Y-%m-%d %H:%M:%S")
		hist+= '</li>'
		hist+= '</ul>'
		hist+= '</div>'
		hist+= '</div>'
	
	return Markup(hist)

if __name__ == "__main__":
	app.run(debug=False,host='0.0.0.0')

