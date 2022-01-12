from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///preliminaryestimate.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db = Database.db # add this line in all models.py files 

class TargetPreliminaryEstimate(db.Model):
	''' target table'''
	__tablename__ = 'targetpreliminaryestimate'

	serialno = db.Column(db.Integer, primary_key=True)
	
	projectid = db.Column(db.String(40))
	responsiblerole = db.Column(db.String(20))
	authoritysubmittedestimate = db.Column(db.String(40))
	authoritysubmittedestimateempid = db.Column(db.String(8))
	
	estimatetype = db.Column(db.String(20))
	peamount = db.Column(db.Integer())
	pecivilamount = db.Column(db.Integer())
	peelectamount = db.Column(db.Integer())
	pehortamount = db.Column(db.Integer())

	stipulatedcompletiondate = db.Column(db.DateTime)
	completiondate = db.Column(db.DateTime)

	pecivilauthority = db.Column(db.String(40))
	pecivilauthorityempid = db.Column(db.String(8))
	peelectauthority = db.Column(db.String(40))
	peelectauthorityempid = db.Column(db.String(8))
	pehortauthority = db.Column(db.String(40))
	pehortauthorityempid = db.Column(db.String(8))
	
	pecivilactdate = db.Column(db.DateTime)
	peelectactdate = db.Column(db.DateTime)
	pehortactdate = db.Column(db.DateTime)
	peremarks = db.Column(db.String(200))

class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()