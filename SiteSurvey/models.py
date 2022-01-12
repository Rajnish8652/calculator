#from datetime import datetime
#from appforms import db
#from sqlalchemy import Column, Integer, DateTime, ForeignKey

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sitesurvey.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db = Database.db # add this line in all models.py files

class TargetSiteSurveyDataMigration(db.Model):
	''' target table'''
	__tablename__ = 'targetsitesurveydatamigration'

	serialno = db.Column(db.Integer, primary_key=True)
	
	projectid = db.Column(db.String(40))
	responsiblerole = db.Column(db.String(20))
	filenumber = db.Column(db.String(40))
	
	authorityapprovedsitesurvey = db.Column(db.String(40))
	authorityapprovedsitesurveyempid = db.Column(db.String(8))
	
	nameofagency = db.Column(db.String(40))
	nameofwork = db.Column(db.String(40))
	
	workorderoragreementnumber = db.Column(db.Integer())
	workorderortenderamount = db.Column(db.Integer())
	
	sitesurveyreportsubmittedbyagency = db.Column(db.String(40))
	stipulateddateofcompletion = db.Column(db.DateTime)
	actualdateofcompletion = db.Column(db.DateTime)

class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()