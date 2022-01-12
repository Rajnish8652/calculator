from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///openpo.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db = Database.db # add this line in all models.py files 

class TargetOpenPurchaseOrder(db.Model):
	''' target table'''
	__tablename__ = 'targetopenpurchaseorder'
	
	serialno = db.Column(db.Integer, primary_key=True) 
	purchasingdocumenttype=db.Column(db.String(4)) 
	companycode=db.Column(db.String(4)) 
	purchasingdocumentcategory=db.Column(db.String(1)) 
	documentdate=db.Column(db.DateTime) 
	vendorsaccountnumber=db.Column(db.String(10)) 
	termsofpayment=db.Column(db.String(4)) 
	purchaseorganization=db.Column(db.String(4)) 
	purchasinggroup=db.Column(db.String(3)) 
	startofvalidityperiod=db.Column(db.DateTime) 
	endofvalidityperiod=db.Column(db.DateTime) 
	iteminpurchasingdocument=db.Column(db.String(5)) 
	materialnumber=db.Column(db.String(40)) 
	plant=db.Column(db.String(4)) 
	storagelocation=db.Column(db.String(4)) 
	purchaseorderquantity=db.Column(db.String(13)) 
	netprice=db.Column(db.String(11)) 
	taxonsalespurchasescode=db.Column(db.String(2)) 
	accountassignmentcategory=db.Column(db.String(1)) 
	wbselement=db.Column(db.String(8)) 
	itemdeliverydate=db.Column(db.DateTime)
	
class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()