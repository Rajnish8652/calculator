#from datetime import datetime
#from appforms import db
#from sqlalchemy import Column, Integer, DateTime, ForeignKey


from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from fintercept.db import Database #add this in all models.py file 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///submissiondrawing.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db = Database.db # add this line in all models.py files

class TargetSubmissionDrawing(db.Model):
	''' target table'''
	__tablename__ = 'targetsubmissiondrawing'

	serialno = db.Column(db.Integer, primary_key=True) 
	projectid=db.Column(db.String(40)) 
	requisitionno=db.Column(db.String(40)) 
	nocfromdirectorateofestate=db.Column(db.String(40)) 
	uploadnocfromdirectorate=db.Column(db.String(100)) 
	principleapprovalfilenumber=db.Column(db.String(40)) 
	uploadprincipleapproval=db.Column(db.String(100)) 
	nocforheightfromairport=db.Column(db.String(40)) 
	uploadnocforheightfromairport=db.Column(db.String(100)) 
	nocfromlndo=db.Column(db.String(40)) 
	uploadnocfromlndo=db.Column(db.String(100)) 
	nocfromnma=db.Column(db.String(40)) 
	uploadnocfromnma=db.Column(db.String(100)) 
	approvalfromforest=db.Column(db.String(40)) 
	uploadapprovalfromforest=db.Column(db.String(100)) 
	approvalfromheritage=db.Column(db.String(40)) 
	uploadapprovalfromheritage=db.Column(db.String(100)) 
	approvalfromcvc=db.Column(db.String(40)) 
	uploadapprovalfromcvc=db.Column(db.String(100)) 
	nocfromdmrc=db.Column(db.String(40)) 
	uploadnocfromdmrc=db.Column(db.String(100)) 
	nocfromgnctd=db.Column(db.String(40)) 
	uploadnocfromgnctd=db.Column(db.String(100)) 
	nocfrommcd=db.Column(db.String(40)) 
	uploadnocfrommcd=db.Column(db.String(100)) 
	nocfromdtp=db.Column(db.String(40)) 
	uploadnocfromdtp=db.Column(db.String(100)) 
	approvalffromuttipecfn=db.Column(db.String(40)) 
	uploadapprovalffromuttipecfn=db.Column(db.String(100)) 
	approvalfromfireofficer=db.Column(db.String(40)) 
	uploadapprovalfromfireofficer=db.Column(db.String(100)) 
	approvalfromcontrollerofexplosives=db.Column(db.String(40)) 
	uploadapprovalfromcontrollerofexplosives=db.Column(db.String(100)) 
	approvalfromchiefoffactories=db.Column(db.String(40)) 
	uploadapprovalfromfactories=db.Column(db.String(100)) 
	approvalfromduac=db.Column(db.String(40)) 
	uploadapprovalfromduac=db.Column(db.String(100)) 
	clearancefrommef=db.Column(db.String(40)) 
	uploadclearancefrommef=db.Column(db.String(100)) 
	nocfromdcp=db.Column(db.String(40)) 
	uploadnocfromdcp=db.Column(db.String(100)) 
	advisefromnsadvisorycommittee=db.Column(db.String(40)) 
	uploadadvisefromnsadvisorycommittee=db.Column(db.String(100)) 
	approvalfromndmc=db.Column(db.String(40)) 
	uploadapprovalfromndmc=db.Column(db.String(100)) 
	buildingplan=db.Column(db.String(40)) 
	uploadbuildingplan=db.Column(db.String(100)) 
	landscapeplan=db.Column(db.String(40)) 

	uploadlandscapeplan=db.Column(db.String(100)) 
	parkingplan=db.Column(db.String(40)) 
	uploadparkingplan=db.Column(db.String(100)) 
	watersupplysewage=db.Column(db.String(40)) 
	uploadwatersupply=db.Column(db.String(100)) 
	layoutplanwherever=db.Column(db.String(40)) 
	uploadlayoutplan=db.Column(db.String(100)) 
	othermiscdrawing=db.Column(db.String(40)) 
	uploadothermisc=db.Column(db.String(100)) 
	
class Log(db.Model):
	''' Log table'''
	__tablename__ = 'logs'
	logid = db.Column(db.String(25), primary_key=True)
	update = db.Column(db.String(255))
	update_time = db.Column(db.DateTime, default=datetime.utcnow)

#db.create_all()
#db.session.commit()