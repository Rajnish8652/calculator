
import imp
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField,DecimalField,TextAreaField,StringField,RadioField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf,NumberRange,regexp
from models import TargetSiteRegister
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file,session
from wtforms import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
import csv
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///siteregister.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class sitereigisterform(FlaskForm):
    client= StringField('Client',validators=[InputRequired('Enter required value !'),Length(max=3),regexp('\d{1,3}')])
    materialdocument= StringField('Material Document',validators=[InputRequired('Enter required value !'),Length(max=8),regexp('\d{1,10}')])
    materialdocyear= DateField('Material Doc Year',format='%Y-%m-%d')
    materialdocitem= StringField('Material Doc.Item',validators=[InputRequired('Enter required value !'),Length(max=8),regexp('\d{1,4}')])
    movementtype= StringField('Movement type',validators=[InputRequired('Enter required value !'),Length(max=3)])
    material= StringField('Material',validators=[InputRequired('Enter required value !'),Length(max=18)])
    plant= StringField('Plant',validators=[InputRequired('Enter required value !'),Length(max=4)])
    storagelocation= StringField('Storage Location',validators=[InputRequired('Enter required value !'),Length(max=4)])
    batch= StringField('Batch',validators=[InputRequired('Enter required value !'),Length(max=10),regexp('\d{1,10}')])
    specialstock= StringField('Special Stock',validators=[InputRequired('Enter required value !'),Length(max=2)])
    supplier= StringField('Supplier',validators=[InputRequired('Enter required value !'),Length(max=10),regexp('\d{1,10}')])
    baseunitofmeasure= StringField('Base Unit of Measure',validators=[InputRequired('Enter required value !'),Length(max=3)])
    storagelocation1= StringField('Storage Location',validators=[Length(max=4)])
    dateofexp= DateField('Date Of Exp',format='%Y-%m-%d')
    qtyinunitofentry=StringField('Qty in unit of Entry',validators=[InputRequired('Enter required value !'),Length(max=10)])
    text= StringField('Text',validators=[InputRequired('Enter required value !'),Length(max=20)])
    goodsrecipient= StringField('Goods Recipient',validators=[Length(max=20)])
    postingdate= DateField('Posting Date',format='%Y-%m-%d')
    entrydate= DateField('Entry Date',format='%Y-%m-%d')
    projectsid= StringField('Projects ID',validators=[InputRequired('Enter required value !'),Length(max=15)])
    projectsname= StringField('Projects Name ',validators=[InputRequired('Enter required value !'),Length(max=20)])
    wbsid= StringField('WBS ID',validators=[InputRequired('Enter required value !'),Length(max=15)])
    wbsdescription= StringField('WBS Description ',validators=[InputRequired('Enter required value !'),Length(max=20)])
    plant1= StringField('Plant',validators=[InputRequired('Enter required value !'),Length(max=4)])
    matarial1= StringField('Matarial',validators=[InputRequired('Enter required value !'),Length(max=18)])
    batch1= StringField('Batch',validators=[Length(max=10)])
    dateofexp1= DateField('Date Of Exp',format='%Y-%m-%d')
    supplier1= StringField('Supplier',validators=[Length(max=10),regexp('\d{1,10}')])

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
    detailsdata = TargetSiteRegister.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET','POST'])
def index():
    form = sitereigisterform()
   

    if request.method=='POST':
        print(form.client.data)
        print(form.materialdocument.data)

        if form.validate_on_submit():
            # Save data to DB
            formdata = TargetSiteRegister(
                client= form.client.data,
                materialdocument= form.materialdocument.data,
                materialdocyear= form.materialdocyear.data,
                materialdocitem= form.materialdocitem.data,
                movementtype= form.movementtype.data,
                material= form.material.data,
                plant= form.plant.data,
                storagelocation= form.storagelocation.data,
                batch= form.batch.data,
                specialstock= form.specialstock.data,
                supplier= form.supplier.data,
                baseunitofmeasure= form.baseunitofmeasure.data,
                storagelocation1= form.storagelocation1.data,
                dateofexp= form.dateofexp.data,
                qtyinunitofentry= form.qtyinunitofentry.data,
                text= form.text.data,
                goodsrecipient= form.goodsrecipient.data,
                postingdate= form.postingdate.data,
                entrydate= form.entrydate.data,
                projectsid= form.projectsid.data,
                projectsname= form.projectsname.data,
                wbsid= form.wbsid.data,
                wbsdescription= form.wbsdescription.data,
                plant1= form.plant1.data,
                matarial1= form.matarial1.data,
                batch1= form.batch1.data,
                dateofexp1= form.dateofexp1.data,
                supplier1= form.supplier1.data

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
    

@app.route('/review/<get_companycode>')
def review(get_companycode):
    #data = TargetSoilInvestigation.query.filter_by(projectid=get_projectno).first()
    #sql = text('Select * from targetsitesurveydatamigration where projectid='+ get_projectno)
    #data =db.session.execute(sql)

    formdata =sitereigisterform()
    for data in TargetSiteRegister.query.filter_by(businesspartnergrouping=get_companycode):
        #print("Yes" if data.person=='Y' else "No")
        #print("Yes" if data.organization=='Y' else "No")
        formdata.client.data=data.client
        formdata.materialdocument.data=data.materialdocument
        formdata.materialdocyear.data=data.materialdocyear
        formdata.materialdocitem.data=data.materialdocitem
        formdata.movementtype.data=data.movementtype
        formdata.material.data=data.material
        formdata.plant.data=data.plant
        formdata.storagelocation.data=data.storagelocation
        formdata.batch.data=data.batch
        formdata.specialstock.data=data.specialstock
        formdata.supplier.data=data.supplier
        formdata.baseunitofmeasure.data=data.baseunitofmeasure
        formdata.storagelocation1.data=data.storagelocation1
        formdata.dateofexp.data=data.dateofexp
        formdata.qtyinunitofentry.data=data.qtyinunitofentry
        formdata.text.data=data.text
        formdata.goodsrecipient.data=data.goodsrecipient
        formdata.postingdate.data=data.postingdate
        formdata.entrydate.data=data.entrydate
        formdata.projectsid.data=data.projectsid
        formdata.projectsname.data=data.projectsname
        formdata.wbsid.data=data.wbsid
        formdata.wbsdescription.data=data.wbsdescription
        formdata.plant1.data=data.plant1
        formdata.matarial1.data=data.matarial1
        formdata.batch1.data=data.batch1
        formdata.dateofexp1.data=data.dateofexp1
        formdata.supplier1.data=data.supplier1

    return  render_template("index.html", form = formdata)

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetSiteRegister)
    exportfile = 'SiteRegister.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetSiteRegister.__table__.columns.keys()
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
    