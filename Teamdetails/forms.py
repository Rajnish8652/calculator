from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField, TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash
from models import Category,BasicFund,TargetTeamDetail,TeamRole
from wtforms import DateField
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
import csv
import csv
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///teamdetail.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class teamrole(Form):
    rolename = StringField('Role Name')
    responsibleresource = StringField('Responsible Resource')
    employeeid = StringField('Employee ID')

class teamdetailForm(FlaskForm):
    projectno = StringField('Project No',validators=[InputRequired('Project No is required!')])
    projectname = StringField('Project Name',validators=[InputRequired('Project Name is required!')])
    description = StringField('Description',render_kw={"placeholder": "Description"})
    category = SelectField('Category',choices=[])
    basisfund = SelectField('Basic Fund',choices=[])
    areastate = StringField('Area / State')
    location = StringField('Location')
    responsiblerole = StringField('Responsible Role')
    responsibleorganizationunit = StringField('Responsible Organisation Unit')
    teamuser = StringField('User')
    #teams = FieldList(FormField(teamrole), min_entries=1)

#---------------Utility Methods---------------
def cleardata(form):
    form.projectno.data=""
    form.projectname.data=""
    form.description.data=""
    form.category.data=""
    form.basisfund.data=""
    form.areastate.data=""
    form.location.data=""
    form.responsiblerole.data=""
    form.responsibleorganizationunit.data=""
    form.teamuser.data=""

#----------------ROUTES SECTION------------------
@app.route('/addrecord/<newrecord>')
def addrecord(newrecord):
    print(type(newrecord))
    newrecord = newrecord.split(',')
    print(type(newrecord))
    print(len(newrecord))

    if (len(newrecord) > 1):
        for x in newrecord:
            print (x)

    return jsonify(newrecord)


# route to the Landing Page
@app.route('/', methods=['GET'])
def main():
    detailsdata = TargetTeamDetail.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET', 'POST'])
def index():
    form = teamdetailForm()
    
    form.category.choices =[("", " Select Type of Work ")] + [(c.cid, c.typeofwork) for c in Category.query.all()]    
    form.basisfund.choices =[("", " Select Basic Fund ")] + [(b.bid, b.basicfunddesc) for b in BasicFund.query.all()]    
            
    if request.method=='POST':
        if form.validate_on_submit():
            projectdata = TargetTeamDetail(
                projectno=form.projectno.data,
                projectname=form.projectname.data,
                description=form.description.data,
                category= dict(form.category.choices).get(form.category.data),
                basisfund=dict(form.basisfund.choices).get(form.basisfund.data),
                areastate=form.areastate.data,
                location=form.location.data,
                responsiblerole=form.responsiblerole.data,
                responsibleorganizationunit=form.responsibleorganizationunit.data,
                teamuser=form.teamuser.data
                )

            rollname=request.form.getlist('item_1[]')
            respres=request.form.getlist('item_2[]')  
            empid=request.form.getlist('item_3[]')
            data= {'teamRoles': [{'rollname': x, 'respres': y,'empid':z} for x, y,z in zip(rollname, respres,empid)]}
            #print (json.dumps(data))

            db.session.add(projectdata)
            #db.session.commit()
            #lastSerialNo = projectdata.serialno 
            #print(str(lastSerialNo))

            for x in data['teamRoles']:
                rollsdata = TeamRole(
                    projectno = form.projectno.data,
                    rolename = x['rollname'],
                    responsibleresource = x['respres'],
                    employeeid = x['empid']
                    )
                db.session.add(rollsdata)
            
            db.session.commit()

            cleardata(form)
            #for k, v in form.data.items():
                #print(k, v)
            
            
            flash(f'TeamDetail Record has Submitted !', 'success')
            redirect(url_for('index'))

            if form.errors != {}: #If there are not errors from the validations
                for err_msg in form.errors.values():
                    flash(f'Failed to Submit Record : {err_msg}', category='danger')
    
    return render_template('index.html', form=form)

@app.route('/review/<get_projectno>')
def review(get_projectno):
    formdata =teamdetailForm()
    formdata.category.choices =[("", " Select Type of Work ")] + [(c.cid, c.typeofwork) for c in Category.query.all()]    
    formdata.basisfund.choices =[("", " Select Basic Fund ")] + [(b.bid, b.basicfunddesc) for b in BasicFund.query.all()]    

    for data in TargetTeamDetail.query.filter_by(projectno=get_projectno):
        formdata.category.default=list(dict(formdata.category.choices).keys())[list(dict(formdata.category.choices).values()).index(data.category)]
        formdata.basisfund.default=list(dict(formdata.basisfund.choices).keys())[list(dict(formdata.basisfund.choices).values()).index(data.basisfund)]
        formdata.process()

        formdata.projectno.data=data.projectno
        formdata.projectname.data=data.projectname
        formdata.description.data=data.description
      
        formdata.areastate.data=data.areastate
        formdata.location.data=data.location
        
        formdata.responsiblerole.data=data.responsiblerole
        formdata.responsibleorganizationunit.data=data.responsibleorganizationunit
        formdata.teamuser.data=data.teamuser

    rolesdata=TeamRole.query.filter_by(projectno=get_projectno)

    return  render_template("index.html", form = formdata,rolesdata=rolesdata)


@app.route('/teamdata/<get_projectno>')
def projectdata(get_projectno):
    #projectdata = TargetTeamDetail.query.filter_by(projectno=get_projectno).first()
    sql = text('Select * from targetteamdetail where projectno='+ get_projectno)
    projectdata =db.session.execute(sql)
    
    #if projectdata.count() > 0 :
    for item in projectdata:
        obj1 = {}
        obj1['projectno'] = item.projectno
        obj1['projectname'] = item.projectname
        obj1['description'] = item.description
        obj1['category'] = item.category
        obj1['basisfund'] = item.basisfund
        obj1['responsiblerole'] = item.responsiblerole
        obj1['responsibleorganizationunit'] = item.responsibleorganizationunit
    
    sql = text('Select * from roledetail where projectno='+ get_projectno)
    roledata =db.session.execute(sql)
    roleArray = []
    for role in roledata:
        obj2 = {}
        obj2['rolename'] = role.rolename
        obj2['responsibleresource'] = role.responsibleresource
        obj2['employeeid'] = role.employeeid
        roleArray.append(obj2)
    
    obj1['roledetail']=roleArray
    return jsonify(obj1)  
    #else:
    #    return 'No Data'

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetTeamDetail)
    exportfile = 'teamdetails.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetTeamDetail.__table__.columns.keys()
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
    
    
    
    






    
