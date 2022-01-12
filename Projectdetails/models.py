from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from fintercept.db import Database #add this in all models.py file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///projectdetail.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db = Database.db # add this line in all models.py files

class Category(db.Model):
	__tablename__ = 'category'

	cid = db.Column(db.String(25), primary_key=True)
	typeofwork = db.Column(db.String(256))

class BasicFund(db.Model):
	__tablename__ = 'basicfund'

	bid = db.Column(db.String(25), primary_key=True)
	basicfunddesc = db.Column(db.String(256))

class ProjectMode(db.Model):
	__tablename__ = 'projectmode'

	pid = db.Column(db.String(25), primary_key=True)
	projectmode = db.Column(db.String(256))

class TargetProjectDetail(db.Model):
	''' Target table'''
	__tablename__ = 'targetprojectdetail'

	serialno = db.Column(db.Integer, primary_key=True)
	projectno = db.Column(db.String(125))
	projectname = db.Column(db.String(256))
	description = db.Column(db.String(256))
	category = db.Column(db.String(256))
	basisfund = db.Column(db.String(256))
	projectmode = db.Column(db.String(256))
	areastate = db.Column(db.String(256))
	location = db.Column(db.String(256))
	actualstart = db.Column(db.DateTime)
	actualfinish = db.Column(db.DateTime)
	forecaststart = db.Column(db.DateTime)
	forecastfinish = db.Column(db.DateTime)
	plannedStart = db.Column(db.DateTime)
	plannedfinish = db.Column(db.DateTime)
	responsibleresource = db.Column(db.String(256))
	responsiblerole = db.Column(db.String(256))
	responsibleorganizationunit = db.Column(db.String(256))
	division1 = db.Column(db.String(256))
	division2 = db.Column(db.String(256))
	division3 = db.Column(db.String(256))
	division4 = db.Column(db.String(256))
	division5 = db.Column(db.String(256))


#class TargetProjectDetailSchema(SQLAlchemyAutoSchema):
#	class Meta:
#		model = TargetProjectDetail

class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)

	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()