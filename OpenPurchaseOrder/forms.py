from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField,IntegerField,DecimalField,TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf,NumberRange,regexp
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file,session
from models import TargetOpenPurchaseOrder
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
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///openpo.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class openpurchaseorderform(FlaskForm):
    purchasingdocumenttype= StringField('Purchasing Document Type',validators=[Length(max=4)])
    companycode= StringField('Company Code',validators=[InputRequired('Company Code is required!'),Length(max=4)])
    purchasingdocumentcategory= StringField('Purchasing Document Category',validators=[Length(max=1)])
    documentdate= DateField('Document Date',format='%Y-%m-%d',default=datetime.today)
    vendorsaccountnumber= StringField("Vendor's Account Number",validators=[Length(max=10)])
    termsofpayment= StringField('Terms of Payment',validators=[Length(max=4)])
    purchaseorganization= StringField('Purchase Organization',validators=[Length(max=4)])
    purchasinggroup= StringField('Purchasing Group',validators=[Length(max=3)])
    startofvalidityperiod= DateField('Start of Validity Period',format='%Y-%m-%d',default=datetime.today)
    endofvalidityperiod= DateField('End of Validity Period',format='%Y-%m-%d',default=datetime.today)
    iteminpurchasingdocument= StringField('Item in Purchasing Document',validators=[Length(max=5)])
    materialnumber= StringField('Material Number',validators=[Length(max=40)])
    plant= StringField('Plant',validators=[Length(max=4)])
    storagelocation= StringField('Storage location',validators=[Length(max=4)])
    purchaseorderquantity= StringField('Purchase Order Quantity',validators=[Length(max=13)])
    netprice= StringField('Net Price',validators=[Length(max=11)])
    taxonsalespurchasescode= StringField('Tax on Sales/ Purchases Code',validators=[Length(max=2)])
    accountassignmentcategory= StringField('Account Assignment Category',validators=[Length(max=1)])
    wbselement= StringField('WBS Element',validators=[Length(max=8)])
    itemdeliverydate= DateField('Item Delivery Date',format='%Y-%m-%d',default=datetime.today)


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
    detailsdata = TargetOpenPurchaseOrder.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET','POST'])
def index():
    form = openpurchaseorderform()

    if request.method=='POST':
        if form.validate_on_submit():
            # Save data to DB
            formdata = TargetOpenPurchaseOrder(
                purchasingdocumenttype= form.purchasingdocumenttype.data,
                companycode= form.companycode.data,
                purchasingdocumentcategory= form.purchasingdocumentcategory.data,
                documentdate= form.documentdate.data,
                vendorsaccountnumber= form.vendorsaccountnumber.data,
                termsofpayment= form.termsofpayment.data,
                purchaseorganization= form.purchaseorganization.data,
                purchasinggroup= form.purchasinggroup.data,
                startofvalidityperiod= form.startofvalidityperiod.data,
                endofvalidityperiod= form.endofvalidityperiod.data,
                iteminpurchasingdocument= form.iteminpurchasingdocument.data,
                materialnumber= form.materialnumber.data,
                plant= form.plant.data,
                storagelocation= form.storagelocation.data,
                purchaseorderquantity= form.purchaseorderquantity.data,
                netprice= form.netprice.data,
                taxonsalespurchasescode= form.taxonsalespurchasescode.data,
                accountassignmentcategory= form.accountassignmentcategory.data,
                wbselement= form.wbselement.data,
                itemdeliverydate= form.itemdeliverydate.data
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

    formdata =openpurchaseorderform()
    for data in TargetOpenPurchaseOrder.query.filter_by(companycode=get_companycode):
        formdata.purchasingdocumenttype.data=data.purchasingdocumenttype
        formdata.companycode.data=data.companycode
        formdata.purchasingdocumentcategory.data=data.purchasingdocumentcategory
        formdata.documentdate.data=data.documentdate
        formdata.vendorsaccountnumber.data=data.vendorsaccountnumber
        formdata.termsofpayment.data=data.termsofpayment
        formdata.purchaseorganization.data=data.purchaseorganization
        formdata.purchasinggroup.data=data.purchasinggroup
        formdata.startofvalidityperiod.data=data.startofvalidityperiod
        formdata.endofvalidityperiod.data=data.endofvalidityperiod
        formdata.iteminpurchasingdocument.data=data.iteminpurchasingdocument
        formdata.materialnumber.data=data.materialnumber
        formdata.plant.data=data.plant
        formdata.storagelocation.data=data.storagelocation
        formdata.purchaseorderquantity.data=data.purchaseorderquantity
        formdata.netprice.data=data.netprice
        formdata.taxonsalespurchasescode.data=data.taxonsalespurchasescode
        formdata.accountassignmentcategory.data=data.accountassignmentcategory
        formdata.wbselement.data=data.wbselement
        formdata.itemdeliverydate.data=data.itemdeliverydate

    return  render_template("index.html", form = formdata)

@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetOpenPurchaseOrder)
    exportfile = 'OpenPurchaseOrder.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetOpenPurchaseOrder.__table__.columns.keys()
            outcsv.writerow(header)     

            for record in exportdata.all():
                outcsv.writerow([getattr(record, c) for c in header ])    

        #return Response(outcsv, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=student_report.xlsx"})    
        flash(f'File Exported as {exportfile} !', 'success')
    else:
        flash(f' Sorry !!!  No Record to Export ', 'danger')

    return redirect(url_for('main'))  #f'<h1> File Saved as {file} ! </h1>' 

if __name__=='__main__':
    app.run(debug=True,port=5000)