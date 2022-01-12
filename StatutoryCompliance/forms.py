from distutils.log import debug
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField, TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash
from models import TargetStatutoryCompliance
from wtforms import DateField
from sqlalchemy import and_, or_, not_
import datetime
from sqlalchemy import text
import csv
from flask_sqlalchemy import SQLAlchemy 
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also  

 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///statutorycompliance.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class statutorycomplianceForm(FlaskForm):
    projectid= StringField('Project ID',validators=[InputRequired('Project No is required!'),Length(max=24)])
    nameofcontractor= StringField('Name of Contractor',validators=[Length(max=18)])
    contractwonumber= StringField('Contract/WO Number',validators=[Length(max=18)])

class statutorycompliancedetails(Form):   
    statutorycompliancedesc= StringField(validators=[Length(max=20)])
    referenceno= StringField(validators=[Length(max=10)])
    validdate= DateField(format='%Y-%m-%d')
    nameofauthorityapproved= StringField(validators=[Length(max=20)])
    employeeidofauthority= StringField(validators=[Length(max=24)]) 

#---------------Utility Methods---------------
def cleardata(form):
    for field in form:
        if field.type == "StringField":
            field.data=""
        elif field.type=="DateField":
            field.data="YYYY-mm-dd"

#----------------ROUTES SECTION------------------
# route to the Landing Page
@app.route('/', methods=['GET'])
def main():
    detailsdata = TargetStatutoryCompliance.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET', 'POST'])
def index():
    form = statutorycomplianceForm()
            
    if request.method=='POST':
        if form.validate_on_submit():
            statutorycompliancedesc=request.form.getlist('item_1[]')
            referenceno=request.form.getlist('item_2[]')  
            validdate=request.form.getlist('item_3[]')
            nameofauthorityapproved=request.form.getlist('item_4[]')
            employeeidofauthority=request.form.getlist('item_5[]')
            data= {'compliancedetails': [{'statutorycompliancedesc': a, 'referenceno': b,'validdate':c,'nameofauthorityapproved':d,'employeeidofauthority':e} 
            for a, b,c,d,e in zip(statutorycompliancedesc, referenceno,validdate,nameofauthorityapproved,employeeidofauthority)]}
            
            for x in data['compliancedetails']:
                #print(datetime.strptime(x['validdate'], "%Y%m%d").date())
                #dat_time = datetime.datetime.strptime(x['validdate']+' 00:00:00','%Y-%m-%d %H:%M:%S')
                
                
                projectdata = TargetStatutoryCompliance(
                    projectid= form.projectid.data,
                    nameofcontractor= form.nameofcontractor.data,
                    contractwonumber= form.contractwonumber.data,
                    statutorycompliancedesc= x['statutorycompliancedesc'], 
                    referenceno= x['referenceno'],
                    validdate= datetime.datetime.strptime(x['validdate']+' 00:00:00', '%Y-%m-%d %H:%M:%S'),   #.strftime('%d-%m-%Y'),
                    nameofauthorityapproved=x['nameofauthorityapproved'],
                    employeeidofauthority= x['employeeidofauthority']
                    )

                db.session.add(projectdata)
                db.session.commit()

            cleardata(form)
            flash(f'TeamDetail Record has Submitted !', 'success')
            redirect(url_for('index'))

            if form.errors != {}: #If there are not errors from the validations
                for err_msg in form.errors.values():
                    flash(f'Failed to Submit Record : {err_msg}', category='danger')
    
    return render_template('index.html', form=form)

@app.route('/review/<get_projectno>')
def review(get_projectno):
    formdata =statutorycomplianceForm()
    compliancedata =statutorycompliancedetails()
    #formdata.category.choices =[("", " Select Type of Work ")] + [(c.cid, c.typeofwork) for c in Category.query.all()]    
   
    for data in TargetStatutoryCompliance.query.filter_by(projectid=get_projectno):
       # formdata.category.default=list(dict(formdata.category.choices).keys())[list(dict(formdata.category.choices).values()).index(data.category)]
       # formdata.basisfund.default=list(dict(formdata.basisfund.choices).keys())[list(dict(formdata.basisfund.choices).values()).index(data.basisfund)]
       # formdata.process()

        formdata.projectid.data=data.projectid
        formdata.nameofcontractor.data=data.nameofcontractor
        formdata.contractwonumber.data=data.contractwonumber
    
    compliancedata=TargetStatutoryCompliance.query.filter_by(projectid=get_projectno)

    return  render_template("index.html", form = formdata,compliancedata=compliancedata)



@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetStatutoryCompliance)
    exportfile = 'StatutoryCompliance.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetStatutoryCompliance.__table__.columns.keys()
            outcsv.writerow(header)     

            for record in exportdata.all():
                outcsv.writerow([getattr(record, c) for c in header ])    

        #return Response(outcsv, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xlsx"})    
        flash(f'File Exported as {exportfile} !', 'success')
    else:
        flash(f' Sorry !!!  No Record to Export ', 'danger')

    return redirect(url_for('main'))  
if __name__=='__main__':
    app.run(debug=True)   
    
    
    
    






    
