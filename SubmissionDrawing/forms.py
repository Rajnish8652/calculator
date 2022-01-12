import os
from flask import Flask
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, IntegerField, TextAreaField,StringField,FormField,FieldList,Form
from wtforms.validators import InputRequired, Length, AnyOf
from models import TargetSubmissionDrawing
from wtforms import DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import render_template, redirect, url_for, flash, request, jsonify, json,session,flash,send_file
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy import and_, or_, not_
from sqlalchemy import text
import csv
from fintercept import Database #add same lines to all the forms.py files 
db = Database.db #add this also 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///submissiondrawing.db"
app.config['SECRET_KEY'] = 'digiko-enc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'appforms\\FileUpload'
app.config["ALLOWED_FILE_EXTENSIONS"] = ["JPEG", "JPG", "PNG","PDF"]
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024   ## 1MB

db = SQLAlchemy(app)


class submissiondrawingForm(FlaskForm):
    projectid= StringField('Project ID',validators=[InputRequired('Project ID is required!'),Length(max=40)])
    requisitionno= StringField('Requisition No',validators=[InputRequired('Requisition No is required!'),Length(max=40)])
    
    nocfromdirectorateofestate= StringField('NOC from Directorate of Estate for Residential Pool Accommodation - File Number',validators=[Length(max=40)])
    uploadnocfromdirectorate= FileField('Upload NOC from Directorate of Estate for Residential Pool Accommodation ',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    principleapprovalfilenumber= StringField('Principle Approval from the Ministry of UD for GPRA File Number',validators=[Length(max=40)])
    uploadprincipleapproval= FileField('Upload Principle Approval from the Ministry of UD for GPRA',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocforheightfromairport= StringField('NOC for height from AIRPORT AUTHORITY OF INDIA File Number',validators=[Length(max=40)])
    uploadnocforheightfromairport= FileField('Upload NOC for Height from AIRPORT AUTHORITY OF INDIA',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromlndo= StringField('NOC from L&DO, when the land is lease-hold File Number',validators=[Length(max=40)])
    uploadnocfromlndo= FileField('Upload No Objection Certificate from L&DO, when the land is lease-hold',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromnma= StringField('NOC from the National Monument Authority (NMA) / ASI File Number',validators=[Length(max=40)])
    uploadnocfromnma= FileField('Upload NOC from the National Monument Authority (NMA) / ASI',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromforest= StringField('APPROVAL FROM FOREST DEPARTMENT File Number',validators=[Length(max=40)])
    uploadapprovalfromforest= FileField('Upload APPROVAL FROM FOREST DEPARTMENT File Number',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromheritage= StringField('APPROVAL FROM HERITAGE CONSERVATION COMMITTEE File Number',validators=[Length(max=40)])
    uploadapprovalfromheritage= FileField('Upload APPROVAL FROM HERITAGE CONSERVATION COMMITTEE File Number',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromcvc= StringField('Approval  from the Central Vista Committee (CVC) File Number',validators=[Length(max=40)])
    uploadapprovalfromcvc= FileField('Upload Approval  from the Central Vista Committee (CVC) ',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromdmrc= StringField('NOC from the Delhi Metro Rail Corporation (DMRC) File Number',validators=[Length(max=40)])
    uploadnocfromdmrc= FileField('Upload NOC from the Delhi Metro Rail Corporation (DMRC)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromgnctd= StringField('NOC  from the Government of National Capital Territory of Delhi (GNCTD) File Number',validators=[Length(max=40)])
    uploadnocfromgnctd= FileField('Upload NOC  from the Government of National Capital Territory of Delhi (GNCTD)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfrommcd= StringField('NOC from the Road Owning Agency (MCD, Delhi PWD, NDMC, DDA) File Number',validators=[Length(max=40)])
    uploadnocfrommcd= FileField('Upload NOC from the Road Owning Agency (MCD, Delhi PWD, NDMC, DDA)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromdtp= StringField('NOC from the Delhi Traffic Police File Number',validators=[Length(max=40)])
    uploadnocfromdtp= FileField('Upload NOC from the Delhi Traffic Police',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalffromuttipecfn= StringField('Approval from UTTIPEC  File Number',validators=[Length(max=40)])
    uploadapprovalffromuttipecfn= FileField('Upload Approval from UTTIPECFN',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromfireofficer= StringField('Approval from CHIEF FIRE OFFICER  File Number ',validators=[Length(max=40)])
    uploadapprovalfromfireofficer= FileField('Upload Approval from CHIEF FIRE OFFICER',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromcontrollerofexplosives= StringField('Approval from the Chief Controller of Explosives, Nagpur File Number',validators=[Length(max=40)])
    uploadapprovalfromcontrollerofexplosives= FileField('Upload Approval from the Chief Controller of Explosives, Nagpur',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromchiefoffactories= StringField('APPROVAL  FROM THE CHIEF Inspector of Factories File Number',validators=[Length(max=40)])
    uploadapprovalfromfactories= FileField('Upload APPROVAL  FROM THE CHIEF Inspector of Factories',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromduac= StringField('APPROVAL IS REQUIRED FROM DELHI URBAN ART COMMISSION (DUAC) File Number',validators=[Length(max=40)])
    uploadapprovalfromduac= FileField('Upload APPROVAL IS REQUIRED FROM DELHI URBAN ART COMMISSION (DUAC)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    clearancefrommef= StringField('ENVIRONMENT CLEARANCE  FROM MINISTRY OF ENVIRONMENT AND FORESTS (MEF)/ State Level Expert Committee File Number',validators=[Length(max=40)])
    uploadclearancefrommef= FileField('Upload ENVIRONMENT CLEARANCE  FROM MINISTRY OF ENVIRONMENT AND FORESTS (MEF)/ State Level Expert Committee ',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    nocfromdcp= StringField('Approval/ NOC from DCP (Licensing) File Number',validators=[Length(max=40)])
    uploadnocfromdcp= FileField('Upload Approval/ NOC from DCP (Licensing)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    advisefromnsadvisorycommittee= StringField('Approval/Advise  from North Block and South Block Advisory Committee File Number',validators=[Length(max=40)])
    uploadadvisefromnsadvisorycommittee= FileField('Upload Approval/Advise  from North Block and South Block Advisory Committee',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    approvalfromndmc= StringField('Approval  from the Power Distributing / Supply Agency (NDMC/ BSES/ NDPL) File Number',validators=[Length(max=40)])
    uploadapprovalfromndmc= FileField('Upload Approval  from the Power Distributing / Supply Agency (NDMC/ BSES/ NDPL)',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    buildingplan= StringField('Building Plans Including Water Harvesting Proposal File Number',validators=[Length(max=40)])
    uploadbuildingplan= FileField('Upload Building Plans Including Water Harvesting Proposal',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    landscapeplan= StringField('Landscape Plan File Number',validators=[Length(max=40)])
    uploadlandscapeplan= FileField('Upload Landscape Plan',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    parkingplan= StringField('Parking Plan File Number',validators=[Length(max=40)])
    uploadparkingplan= FileField('Upload Parking Plan',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    watersupplysewage= StringField('Water Supply,Sewage and Drainage Plans File Number',validators=[Length(max=40)])
    uploadwatersupply= FileField('Upload Water supply,Sewage and Drainage Plans',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    layoutplanwherever= StringField('Layout Plan wherever Applicable File Number',validators=[Length(max=40)])
    uploadlayoutplan= FileField('Upload Layout Plan Wherever Applicable',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])
    othermiscdrawing= StringField('Other Misc.Drawing File Number',validators=[Length(max=40)])
    uploadothermisc= FileField('Upload Other Misc. Drawings',validators=[FileAllowed(['jpg', 'png','pdf'], ' Pdf / Images only!')])

#---------------Utility Methods---------------

def cleardata(form):
    for field in form:
        if field.type == "StringField":
            field.data=""
   

def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]: 
        return True
    else:
        return False    

def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False


def check_uploadpath(foldername):
    CHECK_FOLDER = os.path.isdir(foldername)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(foldername)
        #print('Folder Created !!!') 
              

from uuid import uuid4
def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"

def saveuploadedfile(uploadcopy):
    uploadfilename=""
    
    if uploadcopy== None:
        return uploadfilename

    if uploadcopy.filename != "":
        if allowed_image(uploadcopy.filename):
            filename = secure_filename(uploadcopy.filename)
            upload_dir = os.path.join(os.path.dirname(app.instance_path), app.config['UPLOAD_FOLDER'])
            
            check_uploadpath(upload_dir)

            if (os.path.exists(os.path.join(upload_dir, filename))):
                uploadfilename=make_unique(filename)
            else:
                uploadfilename=filename
                    #dir_path="D:\\Erasmith\\FORMS\\MOUDataMigration\\appforms\\FileUpload"
            uploadcopy.save(os.path.join(upload_dir, uploadfilename))

    return uploadfilename
 

#----------------ROUTES SECTION------------------

# route to the Landing Page
@app.route('/', methods=['GET'])
def main():
    if 'uploadfilename' in session:  
        session.pop('uploadfilename', None)
    detailsdata = TargetSubmissionDrawing.query.all()
    return render_template("main.html", detailsdata = detailsdata)

@app.route('/add', methods=['GET', 'POST'])
def index():
    form = submissiondrawingForm()
    if 'uploadfilename' in session:  
        session.pop('uploadfilename', None)
        
    if request.method=='POST':
        print(form.uploadnocfromlndo.data)

        print(form.uploadapprovalfromforest.data)

        if form.validate_on_submit():
            #uploadfilename=""
            #uploadfilename=saveuploadedfile(form.mouuploadcopy.data)  
            #if (uploadfilename) =="":
            #    return redirect(request.url)

            # Save data to DB
            formdata = TargetSubmissionDrawing(
                projectid= form.projectid.data,
                requisitionno= form.requisitionno.data,
                nocfromdirectorateofestate= form.nocfromdirectorateofestate.data,
                uploadnocfromdirectorate= saveuploadedfile(form.uploadnocfromdirectorate.data), #form.uploadnocfromdirectorate.data,
                principleapprovalfilenumber= form.principleapprovalfilenumber.data,
                uploadprincipleapproval=saveuploadedfile(form.uploadprincipleapproval.data), # form.uploadprincipleapproval.data,
                nocforheightfromairport= form.nocforheightfromairport.data,
                uploadnocforheightfromairport=saveuploadedfile(form.uploadnocforheightfromairport.data), #form.uploadnocforheightfromairport.data,
                nocfromlndo= form.nocfromlndo.data,
                uploadnocfromlndo= saveuploadedfile(form.uploadnocfromlndo.data), #form.uploadnocfromlndo.data,
                nocfromnma= form.nocfromnma.data,
                uploadnocfromnma= saveuploadedfile(form.uploadnocfromnma.data), #form.uploadnocfromnma.data,
                approvalfromforest= form.approvalfromforest.data,
                uploadapprovalfromforest= saveuploadedfile(form.uploadapprovalfromforest.data), #form.uploadapprovalfromforest.data,
                approvalfromheritage= form.approvalfromheritage.data,
                uploadapprovalfromheritage= saveuploadedfile(form.uploadapprovalfromheritage.data), #form.uploadapprovalfromheritage.data,
                approvalfromcvc= form.approvalfromcvc.data,
                uploadapprovalfromcvc= saveuploadedfile(form.uploadapprovalfromcvc.data), #form.uploadapprovalfromcvc.data,
                nocfromdmrc= form.nocfromdmrc.data,
                uploadnocfromdmrc= saveuploadedfile(form.uploadnocfromdmrc.data), #form.uploadnocfromdmrc.data,
                nocfromgnctd= form.nocfromgnctd.data,
                uploadnocfromgnctd= saveuploadedfile(form.uploadnocfromgnctd.data), #form.uploadnocfromgnctd.data,
                nocfrommcd= form.nocfrommcd.data,
                uploadnocfrommcd= saveuploadedfile(form.uploadnocfrommcd.data), #form.uploadnocfrommcd.data,
                nocfromdtp= form.nocfromdtp.data,
                uploadnocfromdtp= saveuploadedfile(form.uploadnocfromdtp.data), #form.uploadnocfromdtp.data,
                approvalffromuttipecfn= form.approvalffromuttipecfn.data,
                uploadapprovalffromuttipecfn= saveuploadedfile(form.uploadapprovalffromuttipecfn.data), #form.uploadapprovalffromuttipecfn.data,
                approvalfromfireofficer= form.approvalfromfireofficer.data,
                uploadapprovalfromfireofficer= saveuploadedfile(form.uploadapprovalfromfireofficer.data), #form.uploadapprovalfromfireofficer.data,
                approvalfromcontrollerofexplosives= form.approvalfromcontrollerofexplosives.data,
                uploadapprovalfromcontrollerofexplosives= saveuploadedfile(form.uploadapprovalfromcontrollerofexplosives.data), #form.uploadapprovalfromcontrollerofexplosives.data,
                approvalfromchiefoffactories= form.approvalfromchiefoffactories.data,
                uploadapprovalfromfactories= saveuploadedfile(form.uploadapprovalfromfactories.data), #form.uploadapprovalfromfactories.data,
                approvalfromduac= form.approvalfromduac.data,
                uploadapprovalfromduac= saveuploadedfile(form.uploadapprovalfromduac.data), #form.uploadapprovalfromduac.data,
                clearancefrommef= form.clearancefrommef.data,
                uploadclearancefrommef= saveuploadedfile(form.uploadclearancefrommef.data), #form.uploadclearancefrommef.data,
                nocfromdcp= form.nocfromdcp.data,
                uploadnocfromdcp= saveuploadedfile(form.uploadnocfromdcp.data), #form.uploadnocfromdcp.data,
                advisefromnsadvisorycommittee= form.advisefromnsadvisorycommittee.data,
                uploadadvisefromnsadvisorycommittee= saveuploadedfile(form.uploadadvisefromnsadvisorycommittee.data), #form.uploadadvisefromnsadvisorycommittee.data,
                approvalfromndmc= form.approvalfromndmc.data,
                uploadapprovalfromndmc= saveuploadedfile(form.uploadapprovalfromndmc.data), #form.uploadapprovalfromndmc.data,
                buildingplan= form.buildingplan.data,
                uploadbuildingplan= saveuploadedfile(form.uploadbuildingplan.data), #form.uploadbuildingplan.data,
                landscapeplan= form.landscapeplan.data,
                uploadlandscapeplan= saveuploadedfile(form.uploadlandscapeplan.data), #form.uploadlandscapeplan.data,
                parkingplan= form.parkingplan.data,
                uploadparkingplan= saveuploadedfile(form.uploadparkingplan.data), #form.uploadparkingplan.data,
                watersupplysewage= form.watersupplysewage.data,
                uploadwatersupply= saveuploadedfile(form.uploadwatersupply.data), #form.uploadwatersupply.data,
                layoutplanwherever= form.layoutplanwherever.data,
                uploadlayoutplan= saveuploadedfile(form.uploadlayoutplan.data), #form.uploadlayoutplan.data,
                othermiscdrawing= form.othermiscdrawing.data,
                uploadothermisc= saveuploadedfile(form.uploadothermisc.data), #form.uploadothermisc.data

                #mouuploadcopy=uploadfilename
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
    formdata =submissiondrawingForm()
    
    if 'uploadfilename' in session:  
        session.pop('uploadfilename', None)

    for data in TargetSubmissionDrawing.query.filter_by(projectid=get_projectno):
        formdata.projectid.data=data.projectid
        formdata.requisitionno.data=data.requisitionno
        formdata.nocfromdirectorateofestate.data=data.nocfromdirectorateofestate
        formdata.uploadnocfromdirectorate.data=data.uploadnocfromdirectorate
        formdata.principleapprovalfilenumber.data=data.principleapprovalfilenumber
        formdata.uploadprincipleapproval.data=data.uploadprincipleapproval
        formdata.nocforheightfromairport.data=data.nocforheightfromairport
        formdata.uploadnocforheightfromairport.data=data.uploadnocforheightfromairport
        formdata.nocfromlndo.data=data.nocfromlndo
        formdata.uploadnocfromlndo.data=data.uploadnocfromlndo
        formdata.nocfromnma.data=data.nocfromnma
        formdata.uploadnocfromnma.data=data.uploadnocfromnma
        formdata.approvalfromforest.data=data.approvalfromforest
        formdata.uploadapprovalfromforest.data=data.uploadapprovalfromforest
        formdata.approvalfromheritage.data=data.approvalfromheritage
        formdata.uploadapprovalfromheritage.data=data.uploadapprovalfromheritage
        formdata.approvalfromcvc.data=data.approvalfromcvc
        formdata.uploadapprovalfromcvc.data=data.uploadapprovalfromcvc
        formdata.nocfromdmrc.data=data.nocfromdmrc
        formdata.uploadnocfromdmrc.data=data.uploadnocfromdmrc
        formdata.nocfromgnctd.data=data.nocfromgnctd
        formdata.uploadnocfromgnctd.data=data.uploadnocfromgnctd
        formdata.nocfrommcd.data=data.nocfrommcd
        formdata.uploadnocfrommcd.data=data.uploadnocfrommcd
        formdata.nocfromdtp.data=data.nocfromdtp
        formdata.uploadnocfromdtp.data=data.uploadnocfromdtp
        formdata.approvalffromuttipecfn.data=data.approvalffromuttipecfn
        formdata.uploadapprovalffromuttipecfn.data=data.uploadapprovalffromuttipecfn
        formdata.approvalfromfireofficer.data=data.approvalfromfireofficer
        formdata.uploadapprovalfromfireofficer.data=data.uploadapprovalfromfireofficer
        formdata.approvalfromcontrollerofexplosives.data=data.approvalfromcontrollerofexplosives
        formdata.uploadapprovalfromcontrollerofexplosives.data=data.uploadapprovalfromcontrollerofexplosives
        formdata.approvalfromchiefoffactories.data=data.approvalfromchiefoffactories
        formdata.uploadapprovalfromfactories.data=data.uploadapprovalfromfactories
        formdata.approvalfromduac.data=data.approvalfromduac
        formdata.uploadapprovalfromduac.data=data.uploadapprovalfromduac
        formdata.clearancefrommef.data=data.clearancefrommef
        formdata.uploadclearancefrommef.data=data.uploadclearancefrommef
        formdata.nocfromdcp.data=data.nocfromdcp
        formdata.uploadnocfromdcp.data=data.uploadnocfromdcp
        formdata.advisefromnsadvisorycommittee.data=data.advisefromnsadvisorycommittee
        formdata.uploadadvisefromnsadvisorycommittee.data=data.uploadadvisefromnsadvisorycommittee
        formdata.approvalfromndmc.data=data.approvalfromndmc
        formdata.uploadapprovalfromndmc.data=data.uploadapprovalfromndmc
        formdata.buildingplan.data=data.buildingplan
        formdata.uploadbuildingplan.data=data.uploadbuildingplan
        formdata.landscapeplan.data=data.landscapeplan
        formdata.uploadlandscapeplan.data=data.uploadlandscapeplan
        formdata.parkingplan.data=data.parkingplan
        formdata.uploadparkingplan.data=data.uploadparkingplan
        formdata.watersupplysewage.data=data.watersupplysewage
        formdata.uploadwatersupply.data=data.uploadwatersupply
        formdata.layoutplanwherever.data=data.layoutplanwherever
        formdata.uploadlayoutplan.data=data.uploadlayoutplan
        formdata.othermiscdrawing.data=data.othermiscdrawing
        formdata.uploadothermisc.data=data.uploadothermisc

        #formdata.mouuploadcopy.data=data.mouuploadcopy
        #session['uploadfilename'] = str(data.mouuploadcopy)

    return  render_template("index.html", form = formdata)


@app.route('/downloadfile')
def downloadfile():
    uploadfilename=session['uploadfilename'] 
    downloadfile="FileUpload\\"+uploadfilename
    return send_file(downloadfile,as_attachment=True)

    
@app.route('/excel', methods=['GET', 'POST'])    
def export():
    exportdata = db.session.query(TargetSubmissionDrawing)
    exportfile = 'SubmissionDrawing.csv'

    if (exportdata.count() > 0): 
        with open(exportfile, 'w') as csvfile:
            outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
            header = TargetSubmissionDrawing.__table__.columns.keys()
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