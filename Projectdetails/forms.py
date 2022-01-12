from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField, TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,Response
from models import Category,BasicFund,ProjectMode,TargetProjectDetail
from wtforms import DateField
from sqlalchemy import and_, or_, not_
import csv
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 

 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///projectdetail.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#ma = Marshmallow(app)


# MainPage Selection Headings
class projectdetailForm(FlaskForm):
    
    projectno = StringField('Project No',validators=[InputRequired('Project No is required!')])
    projectname = StringField('Project Name',validators=[InputRequired('Project Name is required!')])
    description = StringField('Description',render_kw={"placeholder": "Description"})
    category = SelectField('Category',choices=[])
    basisfund = SelectField('Basic Fund',choices=[])
    projectmode = SelectField('Project Mode',choices=[])
    areastate = StringField('Area / State')
    location = StringField('Location')
    actualstart = DateField('Actual Start',format='%Y-%m-%d')
    actualfinish = DateField('Actual Finish',format='%Y-%m-%d')
    forecaststart = DateField('Forecast Start',format='%Y-%m-%d')
    forecastfinish = DateField('Forecast Finish',format='%Y-%m-%d')
    plannedStart = DateField('Planned Start',format='%Y-%m-%d')
    plannedfinish = DateField('Planned Finish',format='%Y-%m-%d')
    responsibleresource = StringField('Responsible Resource')
    responsiblerole = StringField('Responsible Role')
    responsibleorganizationunit = StringField('Responsible Organisation Unit')
    division1 = StringField('Division 1')
    division2 = StringField('Division 2')
    division3 = StringField('Division 3')
    division4 = StringField('Division 4')
    division5 = StringField('Division 5')



#---------------Utility Methods---------------
def cleardata(form):
    form.projectno.data=""
    form.projectname.data=""
    form.description.data=""
    form.category.data=""
    form.basisfund.data=""
    form.projectmode.data=""
    form.areastate.data=""
    form.location.data=""
    form.actualstart.data=""
    form.actualfinish.data=""
    form.forecaststart.data=""
    form.forecastfinish.data=""
    form.plannedStart.data=""
    form.plannedfinish.data=""
    form.responsibleresource.data=""
    form.responsiblerole.data=""
    form.responsibleorganizationunit.data=""
    form.division1.data=""
    form.division2.data=""
    form.division3.data=""
    form.division4.data=""
    form.division5.data=""

#----------------ROUTES SECTION------------------
# route to the Landing Page
@app.route('/', methods=['GET'])
def main():
    detailsdata = TargetProjectDetail.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET', 'POST'])
def index():
    form = projectdetailForm()

    #form.category.choices =[(" Select Type of Work ")] + [(c.typeofwork) for c in Category.query.all()]    

    form.category.choices =[("", " Select Type of Work ")] + [(c.cid, c.typeofwork) for c in Category.query.all()]    
    form.basisfund.choices =[("", " Select Basic Fund ")] + [(b.bid, b.basicfunddesc) for b in BasicFund.query.all()]    
    form.projectmode.choices =[("", " Select Project Mode ")] + [(p.pid, p.projectmode) for p in ProjectMode.query.all()]  

    if request.method=='POST':
        if form.validate_on_submit():
            #return '<h3>Project No {}. The projectname is {}.'.format(form.projectno.data, form.projectname.data)
            projectdata = TargetProjectDetail(
                projectno=form.projectno.data,
                projectname=form.projectname.data,
                description=form.description.data,
                category= dict(form.category.choices).get(form.category.data),
                basisfund=dict(form.basisfund.choices).get(form.basisfund.data),
                projectmode=dict(form.projectmode.choices).get(form.projectmode.data),
                areastate=form.areastate.data,
                location=form.location.data,
                actualstart=form.actualstart.data,
                actualfinish=form.actualfinish.data,
                forecaststart=form.forecaststart.data,
                forecastfinish=form.forecastfinish.data,
                plannedStart=form.plannedStart.data,
                plannedfinish=form.plannedfinish.data,
                responsibleresource=form.responsibleresource.data,
                responsiblerole=form.responsiblerole.data,
                responsibleorganizationunit=form.responsibleorganizationunit.data,
                division1=form.division1.data,
                division2=form.division2.data,
                division3=form.division3.data,
                division4=form.division4.data,
                division5=form.division5.data
                )
            
            db.session.add(projectdata)
            db.session.commit()
            cleardata(form)
            flash(f'Project Details has Submitted !', 'success')
            redirect(url_for('index'))

            if form.errors != {}: #If there are not errors from the validations
                for err_msg in form.errors.values():
                    flash(f'Failed to Submit Record : {err_msg}', category='danger')
    
    return render_template('index.html', form=form)


@app.route('/review/<get_projectno>')
def review(get_projectno):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    #sql = text('Select * from targetsitesurveydatamigration where projectid='+ get_projectno)
    #data =db.session.execute(sql)

    formdata =projectdetailForm()
    formdata.category.choices =[("", " Select Type of Work ")] + [(c.cid, c.typeofwork) for c in Category.query.all()]    
    formdata.basisfund.choices =[("", " Select Basic Fund ")] + [(b.bid, b.basicfunddesc) for b in BasicFund.query.all()]    
    formdata.projectmode.choices =[("", " Select Project Mode ")] + [(p.pid, p.projectmode) for p in ProjectMode.query.all()] 
    
    for data in TargetProjectDetail.query.filter_by(projectno=get_projectno):
        
        formdata.category.default=list(dict(formdata.category.choices).keys())[list(dict(formdata.category.choices).values()).index(data.category)]
        formdata.basisfund.default=list(dict(formdata.basisfund.choices).keys())[list(dict(formdata.basisfund.choices).values()).index(data.basisfund)]
        formdata.projectmode.default=list(dict(formdata.projectmode.choices).keys())[list(dict(formdata.projectmode.choices).values()).index(data.projectmode)]
        formdata.process()

        formdata.projectno.data=data.projectno
        formdata.projectname.data=data.projectname
        formdata.description.data=data.description
        #formdata.category= dict(formdata.category.choices).get(data.category)
        #formdata.basisfund=dict(formdata.basisfund.choices).get(data.basisfund)
        #formdata.projectmode.data=dict(formdata.projectmode.choices).get(data.projectmode)
        formdata.areastate.data=data.areastate
        formdata.location.data=data.location
        formdata.actualstart.data=data.actualstart
        formdata.actualfinish.data=data.actualfinish
        formdata.forecaststart.data=data.forecaststart
        formdata.forecastfinish.data=data.forecastfinish
        formdata.plannedStart.data=data.plannedStart
        formdata.plannedfinish.data=data.plannedfinish
        formdata.responsibleresource.data=data.responsibleresource
        formdata.responsiblerole.data=data.responsiblerole
        formdata.responsibleorganizationunit.data=data.responsibleorganizationunit
        formdata.division1.data=data.division1
        formdata.division2.data=data.division2
        formdata.division3.data=data.division3
        formdata.division4.data=data.division4
        formdata.division5.data=data.division5

    return  render_template("index.html", form = formdata)


# Verify the Project Data Exist
@app.route('/projectdata/<get_projectno>')
def projectdata(get_projectno):
    #projectdata = TargetProjectDetail.query.filter_by(projectno=get_projectno).first()
    sql = text('Select * from targetprojectdetail where projectno='+ get_projectno)
    projectdata =db.session.execute(sql)
    for item in projectdata:
        obj1 = {}
        obj1['projectno'] = item.projectno
        obj1['projectname'] = item.projectname
        obj1['description'] = item.description
        obj1['category'] = item.category
        obj1['basisfund'] = item.basisfund
        obj1['projectmode'] = item.projectmode
        obj1['areastate'] = item.areastate
        obj1['location'] = item.location
        obj1['actualstart'] = item.actualstart
        obj1['actualfinish'] = item.actualfinish
        obj1['forecaststart'] = item.forecaststart
        obj1['forecastfinish'] = item.forecastfinish
        obj1['plannedStart'] = item.plannedStart
        obj1['plannedfinish'] = item.plannedfinish
        obj1['responsibleresource'] = item.responsibleresource
        obj1['responsiblerole'] = item.responsiblerole
        obj1['responsibleorganizationunit'] = item.responsibleorganizationunit
        obj1['division1'] = item.division1
        obj1['division2'] = item.division2
        obj1['division3'] = item.division3
        obj1['division4'] = item.division4
        obj1['division5'] = item.division5
        
    return jsonify(obj1)  

@app.route('/report')
def report():
    sql = text('Select * from targetprojectdetail limit 2')
    projectdata =db.session.execute(sql)
    dArray = []
    for item in projectdata:
        obj1 = {}
        obj1['projectno'] = item.projectno
        obj1['projectname'] = item.projectname
        obj1['description'] = item.description
        obj1['category'] = item.category
        obj1['basisfund'] = item.basisfund
        obj1['projectmode'] = item.projectmode
        obj1['areastate'] = item.areastate
        obj1['location'] = item.location
        obj1['actualstart'] = item.actualstart
        obj1['actualfinish'] = item.actualfinish
        obj1['forecaststart'] = item.forecaststart
        obj1['forecastfinish'] = item.forecastfinish
        obj1['plannedStart'] = item.plannedStart
        obj1['plannedfinish'] = item.plannedfinish
        obj1['responsibleresource'] = item.responsibleresource
        obj1['responsiblerole'] = item.responsiblerole
        obj1['responsibleorganizationunit'] = item.responsibleorganizationunit
        obj1['division1'] = item.division1
        obj1['division2'] = item.division2
        obj1['division3'] = item.division3
        obj1['division4'] = item.division4
        obj1['division5'] = item.division5
        dArray.append(obj1)

    return jsonify({'tdata': dArray})    
    
def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


#@app.route('/excel', methods=['GET', 'POST'])
#def exportexcel():
    #data = TargetProjectDetail.query.all()
    #data_list = [to_dict(item) for item in data]
    #df = pd.DataFrame(data_list)
    #filename = app.config['UPLOAD_FOLDER']+"/autos.xlsx"
    #print("Filename: "+filename)

    #writer = pd.ExcelWriter(filename)
    #df.to_excel(writer, sheet_name='Registrados')
    #writer.save()

    #return send_file(filename)

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetProjectDetail)
    exportfile = 'projectdetails.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetProjectDetail.__table__.columns.keys()
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







    
