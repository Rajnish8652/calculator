from flask import Flask
from wtforms import SelectField,SubmitField, IntegerField,DecimalField,TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf,NumberRange,regexp
from models import TargetSiteSurveyDataMigration
from wtforms import DateField
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file,session
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
import csv
from flask_sqlalchemy import SQLAlchemy  
from flask_wtf import FlaskForm
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sitesurvey.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class sitesurveydatamigration(FlaskForm):
    projectid = StringField('Project ID',validators=[InputRequired('Project ID is required!'),Length(max=40)])
    #responsiblerole = StringField('Responsible Role',render_kw={"placeholder": "Responsible Role"},validators=[InputRequired(), Length(max=20)])
    responsiblerole = StringField('Responsible Role',validators=[InputRequired(), Length(max=20)])
    filenumber = StringField('File Number',validators=[Length(max=40)])
    
    authorityapprovedsitesurvey = StringField('Authority Approved Site Survey',validators=[InputRequired(), Length(max=40)])
    authorityapprovedsitesurveyempid = StringField('Authority Approved Site Survey Employee Id',validators=[Length(max=8)])
    
    nameofagency = StringField('Name of Agency',validators=[Length(max=40)])
    nameofwork = StringField('Name of Work',validators=[Length(max=40)])
    
    workorderoragreementnumber =StringField('Work Order or Agreement Number',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")]) 
    workorderortenderamount = StringField('Work Order or Tender Amount',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")])
    
    sitesurveyreportsubmittedbyagency = StringField('Site Survey Report Submitted by Agency',validators=[Length(max=40)])
    stipulateddateofcompletion = DateField('Stipulated Date of Completion',format='%Y-%m-%d')
    actualdateofcompletion = DateField('Actual Date of Completion',format='%Y-%m-%d')
    

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
    detailsdata = TargetSiteSurveyDataMigration.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET','POST'])
def index():
    form = sitesurveydatamigration()
    if request.method=='POST':
        if form.validate_on_submit():
            # Save data to DB
            formdata = TargetSiteSurveyDataMigration(
                projectid=form.projectid.data,
                responsiblerole=form.responsiblerole.data,
                filenumber=form.filenumber.data,
                authorityapprovedsitesurvey=form.authorityapprovedsitesurvey.data,
                authorityapprovedsitesurveyempid=form.authorityapprovedsitesurveyempid.data,
                
                nameofagency=form.nameofagency.data,
                nameofwork=form.nameofwork.data,
                workorderoragreementnumber=form.workorderoragreementnumber.data,
                workorderortenderamount=form.workorderortenderamount.data,
                sitesurveyreportsubmittedbyagency=form.sitesurveyreportsubmittedbyagency.data,

                stipulateddateofcompletion=form.stipulateddateofcompletion.data,
                actualdateofcompletion=form.actualdateofcompletion.data,

            )
            
            db.session.add(formdata)
            db.session.commit()

            cleardata(form)

            flash(f'Record has Submitted !', 'success')
            redirect(url_for('main'))
        
            if form.errors != {}: #If there are not errors from the validations
                for err_msg in form.errors.values():
                    flash(f'Failed to Submit Record : {err_msg}', category='danger')
    
    return render_template('index.html', form=form)
    


@app.route('/getdatabyid/<get_projectno>')
def getdatabyid(get_projectno):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    sql = text('Select * from targetsitesurveydatamigration where projectid='+ get_projectno)
    data =db.session.execute(sql)
    print(str(get_projectno))
    return  json.dumps([dict(r) for r in data])

    

@app.route('/review/<get_projectno>')
def review(get_projectno):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    #sql = text('Select * from targetsitesurveydatamigration where projectid='+ get_projectno)
    #data =db.session.execute(sql)

    formdata = sitesurveydatamigration()
    for data in TargetSiteSurveyDataMigration.query.filter_by(projectid=get_projectno):
        
        #print(str(data.projectid))
        #print(str(data.responsiblerole))
        formdata.projectid.data=data.projectid
        formdata.responsiblerole.data=data.responsiblerole
        formdata.filenumber.data=data.filenumber
        formdata.authorityapprovedsitesurvey.data=data.authorityapprovedsitesurvey
        formdata.authorityapprovedsitesurveyempid.data=data.authorityapprovedsitesurveyempid
        formdata.nameofagency.data=data.nameofagency
        formdata.nameofwork.data=data.nameofwork
        formdata.workorderoragreementnumber.data=data.workorderoragreementnumber
        formdata.workorderortenderamount.data=data.workorderortenderamount
        formdata.sitesurveyreportsubmittedbyagency.data=data.sitesurveyreportsubmittedbyagency

        formdata.stipulateddateofcompletion.data=data.stipulateddateofcompletion
        formdata.actualdateofcompletion.data=data.actualdateofcompletion

    return  render_template("index.html", form = formdata)
    
@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetSiteSurveyDataMigration)
    exportfile = 'HouseBank.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetSiteSurveyDataMigration.__table__.columns.keys()
            outcsv.writerow(header)     

            for record in exportdata.all():
                outcsv.writerow([getattr(record, c) for c in header ])    

        #return Response(outcsv, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xlsx"})    
        flash(f'File Exported as {exportfile} !', 'success')
    else:
        flash(f' Sorry !!!  No Record to Export ', 'danger')

    return redirect(url_for('main'))  #f'<h1> File Saved as {file} ! </h1>' 

if __name__=='__main__':
    app.run(debug=True)
    

    
    






    
