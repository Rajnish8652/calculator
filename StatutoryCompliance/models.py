#from datetime import datetime
#from appforms import db
#from sqlalchemy import Column, Integer, DateTime, ForeignKey

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///statutorycompliance.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db = Database.db # add this line in all models.py files
class TargetStatutoryCompliance(db.Model):
	''' Target table'''
	__tablename__ = 'targetstatutorycompliance'

	serialno = db.Column(db.Integer, primary_key=True) 
	projectid=db.Column(db.String(24)) 
	nameofcontractor=db.Column(db.String(18)) 
	contractwonumber=db.Column(db.String(18)) 
	statutorycompliancedesc=db.Column(db.String(20)) 
	referenceno=db.Column(db.String(10)) 
	validdate=db.Column(db.DateTime) 
	nameofauthorityapproved=db.Column(db.String(20)) 
	employeeidofauthority=db.Column(db.String(24))

	
class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()