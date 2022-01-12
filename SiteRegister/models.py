from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///siteregister.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db = Database.db # add this line in all models.py files 

class TargetSiteRegister(db.Model):
	''' target table'''
	__tablename__ = 'targetsiteregister'
	
	serialno = db.Column(db.Integer, primary_key=True) 
	client=db.Column(db.Integer()) 
	materialdocument=db.Column(db.Integer()) 
	materialdocyear=db.Column(db.DateTime) 
	materialdocitem=db.Column(db.Integer()) 
	movementtype=db.Column(db.String(3)) 
	material=db.Column(db.String(18)) 
	plant=db.Column(db.String(4)) 
	storagelocation=db.Column(db.String(4)) 
	batch=db.Column(db.Integer()) 
	specialstock=db.Column(db.String(2)) 
	supplier=db.Column(db.Integer()) 
	baseunitofmeasure=db.Column(db.String(3)) 
	storagelocation1=db.Column(db.String(4)) 
	dateofexp=db.Column(db.DateTime)
	qtyinunitofentry=db.Column(db.Integer()) 
	text=db.Column(db.String(20)) 
	goodsrecipient=db.Column(db.String(20)) 
	postingdate=db.Column(db.DateTime) 
	entrydate=db.Column(db.DateTime) 
	projectsid=db.Column(db.String(15)) 
	projectsname=db.Column(db.String(20)) 
	wbsid=db.Column(db.String(15)) 
	wbsdescription=db.Column(db.String(20)) 
	plant1=db.Column(db.String(4)) 
	matarial1=db.Column(db.String(18)) 
	batch1=db.Column(db.Integer()) 
	dateofexp1=db.Column(db.DateTime) 
	supplier1=db.Column(db.Integer()) 
	
class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()