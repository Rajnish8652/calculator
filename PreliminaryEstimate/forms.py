from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField,DecimalField,TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf,NumberRange,regexp
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file,session
from models import TargetPreliminaryEstimate
from wtforms import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy  
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///preliminaryestimate.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class preliminaryestimateform(FlaskForm):
    projectid = StringField('Project ID',validators=[InputRequired('Project ID is required!'),Length(max=40)])
    responsiblerole = StringField('Responsible Role',validators=[InputRequired(), Length(max=20)])
    authoritysubmittedestimate = StringField('Authority Submitted Estimate',validators=[InputRequired(),Length(max=40)])
    authoritysubmittedestimateempid = StringField('Authority Submitted Estimate Emp ID',validators=[InputRequired(),Length(max=8)])
    
    estimatetype = SelectField(u'Estimate Type',choices=[('',''),('Civil', 'Civil'), ('Electrical', 'Electrical'), ('Horticulture', 'Horticulture'),('Total Project Estimation','Total Project Estimation')])

    peamount = StringField('PE Amount',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")])
    pecivilamount = StringField('PE Civil Amount',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")])
    peelectamount = StringField('PE Elect. Amount',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")])
    pehortamount = StringField('PE Hort. Amount',render_kw={"placeholder": "00000000"}, validators=[Length(max=8),regexp("\d{1,8}")])
    
    stipulatedcompletiondate = DateField('Stipulated Completion Date',format='%Y-%m-%d')
    completiondate = DateField('Completion Date',format='%Y-%m-%d')
    
    pecivilauthority = StringField('PE Civil Authority',validators=[Length(max=40)])
    pecivilauthorityempid = StringField('PE Civil Authority Emp ID',validators=[Length(max=8)])
    
    peelectauthority = StringField('PE Elect Authority',validators=[Length(max=40)])
    peelectauthorityempid = StringField('PE Elect Authority Emp ID',validators=[Length(max=8)])
    
    pehortauthority = StringField('PE Hort Authority',validators=[Length(max=40)])
    pehortauthorityempid = StringField('PE Hort Authority Emp ID',validators=[Length(max=8)])
    
    pecivilactdate = DateField('PE Civil Act Date',format='%Y-%m-%d')
    peelectactdate = DateField('PE Elect Act Date',format='%Y-%m-%d')
    pehortactdate = DateField('PE Hort Act Date',format='%Y-%m-%d')
    peremarks = StringField('PE Remarks',validators=[Length(max=200)])
    

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
    detailsdata = TargetPreliminaryEstimate.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET','POST'])
def index():
    form = preliminaryestimateform()

    if request.method=='POST':
        if form.validate_on_submit():
            # Save data to DB
            formdata = TargetPreliminaryEstimate(
                projectid=form.projectid.data,
                responsiblerole=form.responsiblerole.data,
                authoritysubmittedestimate=form.authoritysubmittedestimate.data,
                authoritysubmittedestimateempid=form.authoritysubmittedestimateempid.data,
                
                estimatetype=form.estimatetype.data,
                peamount=form.peamount.data,
                pecivilamount=form.pecivilamount.data,
                peelectamount=form.peelectamount.data,
                pehortamount=form.pehortamount.data,

                stipulatedcompletiondate=form.stipulatedcompletiondate.data,
                completiondate=form.completiondate.data,

                pecivilauthority=form.pecivilauthority.data,
                pecivilauthorityempid=form.pecivilauthorityempid.data,

                peelectauthority=form.pecivilauthority.data,
                peelectauthorityempid=form.peelectauthorityempid.data,

                pehortauthority=form.pehortauthority.data,
                pehortauthorityempid=form.pehortauthorityempid.data,

                pecivilactdate=form.pecivilactdate.data,
                peelectactdate=form.peelectactdate.data,
                pehortactdate=form.pehortactdate.data,
                peremarks=form.peremarks.data

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
    

@app.route('/review/<get_projectno>')
def review(get_projectno):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    #sql = text('Select * from targetsitesurveydatamigration where projectid='+ get_projectno)
    #data =db.session.execute(sql)

    formdata =preliminaryestimateform()
    for data in TargetPreliminaryEstimate.query.filter_by(projectid=get_projectno):
        formdata.projectid.data=data.projectid
        formdata.responsiblerole.data=data.responsiblerole
        formdata.authoritysubmittedestimate.data=data.authoritysubmittedestimate
        formdata.authoritysubmittedestimateempid.data=data.authoritysubmittedestimateempid

        formdata.estimatetype.data=data.estimatetype
        formdata.peamount.data=data.peamount
        formdata.pecivilamount.data=data.pecivilamount
        formdata.peelectamount.data=data.peelectamount
        formdata.pehortamount.data=data.pehortamount

        formdata.stipulatedcompletiondate.data=data.stipulatedcompletiondate
        formdata.completiondate.data=data.completiondate

        formdata.pecivilauthority.data=data.pecivilauthority
        formdata.pecivilauthorityempid.data=data.pecivilauthorityempid

        formdata.peelectauthority.data=data.pecivilauthority
        formdata.peelectauthorityempid.data=data.peelectauthorityempid

        formdata.pehortauthority.data=data.pehortauthority
        formdata.pehortauthorityempid.data=data.pehortauthorityempid

        formdata.pecivilactdate.data=data.pecivilactdate
        formdata.peelectactdate.data=data.peelectactdate
        formdata.pehortactdate.data=data.pehortactdate
        formdata.peremarks.data=data.peremarks        

    return  render_template("index.html", form = formdata)

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetPreliminaryEstimate)
    exportfile = 'PreliminaryEstimate.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetPreliminaryEstimate.__table__.columns.keys()
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