from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField,DecimalField,TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf,NumberRange,regexp
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file,session
from models import TargetSoilInvestigation
from wtforms import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
import csv
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///soilinvestigation.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class soilinvestigationForm(FlaskForm):
    projectid = StringField('Project ID',validators=[InputRequired('Project ID is required!'),Length(max=40)])
    #responsiblerole = StringField('Responsible Role',render_kw={"placeholder": "Responsible Role'"},validators=[InputRequired(), Length(max=20)])
    responsiblerole = StringField('Responsible Role',validators=[InputRequired(), Length(max=20)])
    authorityapprovedsoilinvestigation = StringField('Authority Approved Soil Investigation',validators=[InputRequired(), Length(max=40)])
    authorityapprovedsoilinvestigationempid = StringField('Authority Approved Soil Investigation Employee Id',validators=[Length(max=8)])
    nameofagency = StringField('Name of Agency',validators=[Length(max=40)])
    nameofwork = StringField('Name of Work',validators=[Length(max=40)])
    workorderoragreementnumber =StringField('Work Order or Agreement Number',validators=[Length(max=8),regexp("\d{1,8}")]) 
    
    filenumber = StringField('File Number',validators=[Length(max=20)])
    workorderortenderamount = StringField('Work Order or Tender Amount',validators=[Length(max=8),regexp("\d{1,8}")])
    stipulateddateofcompletion = DateField('Stipulated Date of Completion',format='%Y-%m-%d')
    actualdateofcompletion = DateField('Actual Date of Completion',format='%Y-%m-%d')
    sitesurveyplansubmittedbyagency = StringField('Site Survey Plan Submitted by Agency',validators=[Length(max=40)])
    typeoftest = StringField('Type of Test',validators=[Length(max=40)])
    typeofsoil = StringField('Type of Soil',validators=[Length(max=40)])
    
    typeoffoundationrecommended = StringField('Type of Foundation Recommended',validators=[Length(max=40)])
    sptvalues = StringField('SPT Values',validators=[Length(max=40)])
    specificgravityofsoil = StringField('Specific Gravity of Soil',validators=[Length(max=40)])
    watertable = StringField('Water Table',validators=[Length(max=40)])
    soilbearingcapacity = StringField('Soil Bearing Capacity',validators=[Length(max=40)])

#---------------Utility Methods---------------

def cleardata(form):
    for field in form:
        if field.type == "StringField":
            field.data=""
        elif field.type=="DateField":
            field.data=""
    
#----------------ROUTES SECTION------------------

# route to the Landing Page
@app.route('/', methods=['GET'])
def main():
    detailsdata = TargetSoilInvestigation.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET', 'POST'])
def index():
    form = soilinvestigationForm()
    
    if request.method=='POST':
        if form.validate_on_submit():
            # Save data to DB
            formdata = TargetSoilInvestigation(
                projectid=form.projectid.data,
                responsiblerole=form.responsiblerole.data,
                authorityapprovedsoilinvestigation=form.authorityapprovedsoilinvestigation.data,
                authorityapprovedsoilinvestigationempid=form.authorityapprovedsoilinvestigationempid.data,
                nameofagency=form.nameofagency.data,
                nameofwork=form.nameofwork.data,
                workorderoragreementnumber=form.workorderoragreementnumber.data,

                filenumber=form.filenumber.data,
                workorderortenderamount=form.workorderortenderamount.data,
                stipulateddateofcompletion=form.stipulateddateofcompletion.data,
                actualdateofcompletion=form.actualdateofcompletion.data,
                sitesurveyplansubmittedbyagency=form.sitesurveyplansubmittedbyagency.data,
                typeoftest=form.typeoftest.data,
                typeofsoil=form.typeofsoil.data,

                typeoffoundationrecommended=form.typeoffoundationrecommended.data,
                sptvalues=form.sptvalues.data,
                specificgravityofsoil=form.specificgravityofsoil.data,
                watertable=form.watertable.data,
                soilbearingcapacity=form.soilbearingcapacity.data

            )
            
            db.session.add(formdata)
            db.session.commit()

            cleardata(form)

            flash(f'Record has Submitted !', 'success')
            redirect(url_for('index'))
        
            if form.errors != {}: #If there are not errors from the validations
                for err_msg in form.errors.values():
                    flash(f'Failed to Submit Record : {err_msg}', category='danger')
    
    return render_template('index.html', form=form)


@app.route('/review/<get_projectno>')
def review(get_projectno):
    formdata =soilinvestigationForm()

    for data in TargetSoilInvestigation.query.filter_by(projectid=get_projectno):
        formdata.projectid.data=data.projectid
        formdata.responsiblerole.data=data.responsiblerole
        formdata.authorityapprovedsoilinvestigation.data=data.authorityapprovedsoilinvestigation
        formdata.authorityapprovedsoilinvestigationempid.data=data.authorityapprovedsoilinvestigationempid
        formdata.nameofagency.data=data.nameofagency
        formdata.nameofwork.data=data.nameofwork
        formdata.workorderoragreementnumber.data=data.workorderoragreementnumber
        formdata.filenumber.data=data.filenumber
        formdata.workorderortenderamount.data=data.workorderortenderamount
        formdata.stipulateddateofcompletion.data=data.stipulateddateofcompletion
        formdata.actualdateofcompletion.data=data.actualdateofcompletion
        formdata.sitesurveyplansubmittedbyagency.data=data.sitesurveyplansubmittedbyagency
        formdata.typeoftest.data=data.typeoftest
        formdata.typeofsoil.data=data.typeofsoil
        formdata.typeoffoundationrecommended.data=data.typeoffoundationrecommended
        formdata.sptvalues.data=data.sptvalues
        formdata.specificgravityofsoil.data=data.specificgravityofsoil
        formdata.watertable.data=data.watertable
        formdata.soilbearingcapacity.data=data.soilbearingcapacity
       
    return  render_template("index.html", form = formdata)


@app.route('/getdatabyid/<get_projectno>')
def getdatabyid(get_projectno):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    sql = text('Select * from targetsoilinvestigation where projectid='+ get_projectno)
    data =db.session.execute(sql)
    print(str(get_projectno))
    return  json.dumps([dict(r) for r in data])
 

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetSoilInvestigation)
    exportfile = 'SoilInvestigation.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetSoilInvestigation.__table__.columns.keys()
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

    


    
    
    






    
