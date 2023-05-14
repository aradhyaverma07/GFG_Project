from flask import Flask,render_template,request,redirect,flash
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , login_user, LoginManager, login_required, logout_user, current_user,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
import json

local_server=True
app = Flask(__name__)
app.secret_key='aradhya'

#with open('config.json','r') as c:
 # params=json.load(c)["params"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:@localhost/covid"
db=SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or Hospitaluser.query.get(int(user_id))


class User(db.Model,UserMixin) :
    id = db.Column(db.Integer, primary_key=True)
    srfid = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(100))
    dob=db.Column(db.String(1000))


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)



class Hospitaluser(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    email=db.Column(db.String(50))
    password=db.Column(db.String(1000))    

class Hospitaldata(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    hname=db.Column(db.String(100))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)
 

class Bookingpatient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    bedtype=db.Column(db.String(100))
    hcode=db.Column(db.String(20))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(100))
    pphone=db.Column(db.String(100))
    paddress=db.Column(db.String(100))

class Trig(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20))
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)
    querys=db.Column(db.String(50))
    date=db.Column(db.String(50))

class Department(db.Model,UserMixin) :
    id = db.Column(db.Integer, primary_key=True)
    depid = db.Column(db.String(50), unique=True)
    depname = db.Column(db.String(50))

class Hospital(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    hcode=db.Column(db.String(20),unique=True)
    hname=db.Column(db.String(100))
    depid = db.Column(db.String(50), unique=True)
    normalbed=db.Column(db.Integer)
    hicubed=db.Column(db.Integer)
    icubed=db.Column(db.Integer)
    vbed=db.Column(db.Integer)
    haddress=db.Column(db.String(100))

class Booking(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    srfid=db.Column(db.String(20),unique=True)
    bedtype=db.Column(db.String(100))
    hcode=db.Column(db.String(20))
    spo2=db.Column(db.Integer)
    pname=db.Column(db.String(100))
    pphone=db.Column(db.String(100))
    paddress=db.Column(db.String(100))
 
class Pharmacy(db.Model,UserMixin) :
    id = db.Column(db.Integer, primary_key=True)
    phid = db.Column(db.String(50), unique=True)
    phname = db.Column(db.String(50))
    hcode=db.Column(db.String(20))


@app.route("/")
def hello_world():
    return render_template('index.html',user=current_user)


@app.route("/trigers")
def trigers():
    query=Trig.query.all() 
    return render_template("trigers.html",query=query)



@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return 'connected'
    except Exception as e:
        print(e)
        return 'not connected'

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        srfid=request.form.get('srf')
        email=request.form.get('email')
        dob=request.form.get('dob')
        encpassword=generate_password_hash(dob) 
        user=User.query.filter_by(srfid=srfid).first()
        emailUser=User.query.filter_by(email=email).first()
        if user or emailUser:
            flash ("Email or srfid is alread taken","warning")
            return render_template('usersignup.html')
        new_user=User(srfid=srfid,email=email,dob=encpassword)
        db.session.add(new_user)
        db.session.commit()
        user1=User.query.filter_by(srfid=srfid).first()

        if user1 and check_password_hash(user1.dob,dob):
            login_user(user1)
            flash("SignIn Successful","success")
            return render_template('userlogin.html')
       
    return render_template('usersignup.html')


@app.route ("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        srfid=request.form.get('srf')
        dob=request.form.get('dob')
        user=User.query.filter_by(srfid=srfid).first()

        if user and check_password_hash(user.dob,dob):
            login_user(user)
            flash("Login Succesful","info")
            return render_template('index.html')
        else:
            flash("Invalid Credentials","danger")
            return render_template('userlogin.html')

    return render_template('userlogin.html')

@app.route("/hospitallogin", methods=['GET', 'POST'])
def hospitallogin():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        hospital=Hospitaluser.query.filter_by(email=email).first()
        if hospital and check_password_hash(hospital.password,password):
            login_user(hospital)
            flash("Login Succesful","info")
            return render_template('index.html')
        else:
            flash("Invalid Credentials","danger")
            return render_template('hospitallogin.html')

    return render_template('hospitallogin.html')


@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        if(username=="aradhya" and password=="aradhya123"):
            session['user']=username
            flash("login success","info")
            return render_template("addHosUser.html")
        else:
            flash("Invalid Credentials","danger")
    return render_template("admin.html")

@app.route('/addHospitalUser',methods=['POST','GET'])
def hospitalUser():
   
    if('user' in session and session['user']=="aradhya"):
      
        if request.method=="POST":
            hcode=request.form.get('hcode')
            email=request.form.get('email')
            password=request.form.get('password')        
            encpassword=generate_password_hash(password)  
            hcode=hcode.upper()       
            emailUser=Hospitaluser.query.filter_by(email=email).first()
            if  emailUser:
                flash("Email or srif is already taken","warning")

           # print(hcode,email,password)    

            new_hospital=Hospitaluser(hcode=hcode,email=email,password=encpassword)
            db.session.add(new_hospital)
            db.session.commit()

           
           # mail.send_message('COVID CARE CENTER',sender=,recipients=[email],body=f"Welcome thanks for choosing us\nYour Login Credentials Are:\n Email Address: {email}\nPassword: {password}\n\nHospital Code {hcode}\n\n Do not share your password\n\n\nThank You..." )

            flash("Data Sent and Inserted Successfully","success")
            return render_template("addHosUser.html")

    else:
        flash("Login and try Again","warning")
        return render_template("addHosUser.html")            


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logout Succesful","warning")
    return redirect(url_for('login'))


@app.route('/logoutadmin', methods=['GET', 'POST'])
@login_required
def logoutadmin():
    logout_user()
    flash("Logout Succesful","warning")
    return redirect("/admin")


@app.route("/addhospitalinfo", methods=['GET', 'POST'])
def addhospitalinfo():
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospitaldata.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubed')
        icubed=request.form.get('icubed')
        vbed=request.form.get('vbed')
        hcode=hcode.upper()
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        hduser=Hospitaldata.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        if huser:            
            new_data=Hospitaldata(hcode=hcode,hname=hname,normalbed=normalbed,hicubed=hicubed,icubed=icubed,vbed=vbed)
            db.session.add(new_data)
            db.session.commit()

            return redirect('/addhospitalinfo')
            

        else:
            flash("Hospital Code not Exist","warning")
            return redirect('/addhospitalinfo')




    return render_template("hospitaldata.html",user=current_user,postsdata=postsdata)


@app.route("/hedit/<string:id>",methods=['POST','GET'])
@login_required
def hedit(id):
    posts=Hospitaldata.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubeds')
        icubed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        hcode=hcode.upper()
        update=Hospitaldata.query.filter_by(id=id).first()
        update.hcode=hcode
        update.hname=hname
        update.normalbed=normalbed
        update.hicubed=hicubed
        update.icubed=icubed
        update.vbed=vbed
        db.session.commit()
        flash("Slot Updated","info")
        return redirect("/addhospitalinfo")

    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hedit.html",posts=posts)


@app.route("/hdelete/<string:id>",methods=['POST','GET'])
@login_required
def hodelete(id):
    dele=Hospitaldata.query.filter_by(id=id).first()
    db.session.delete(dele)
    db.session.commit()
    flash("Date Deleted","danger")
    return redirect("/addhospitalinfo")


@app.route("/slotbooking",methods=['POST','GET'])
@login_required
def slotbooking():
    query1=Hospitaldata.query.all()
    query=Hospitaldata.query.all()   
    if request.method=="POST":        
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospitaldata.query.filter_by(hcode=hcode).first()
        checkpatient=Bookingpatient.query.filter_by(srfid=srfid).first()
        if checkpatient:
            flash("already srd id is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        dbb=Hospitaldata.query.filter_by(hcode=code).first()        
        bedtype=bedtype
        if bedtype=="NormalBed":       
            
                seat=dbb.normalbed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.normalbed=seat-1
                db.session.commit()
                
            
        elif bedtype=="HICUBed":      
 
                seat=dbb.hicubed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.hicubed=seat-1
                db.session.commit()

        elif bedtype=="ICUBed":     

                seat=dbb.icubed
                print(seat)
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.icubed=seat-1
                db.session.commit()

        elif bedtype=="VENTILATORBed": 

                seat=dbb.vbed
                ar=Hospitaldata.query.filter_by(hcode=code).first()
                ar.vbed=seat-1
                db.session.commit()
        else:
            pass

        check=Hospitaldata.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Bookingpatient(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
                db.session.add(res)
                db.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("booking.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("booking.html",query=query,query1=query1,user=current_user)


@app.route("/pdetails",methods=['GET'])
@login_required
def pdetails():
    code=current_user.srfid
    print(code)
    data=Bookingpatient.query.filter_by(srfid=code).first()
    return render_template("details.html",data=data)

@app.route("/noncovid")
def noncovid():
    return render_template('index2.html',user=current_user)

@app.route("/department",methods=['POST','GET'])
@login_required
def department():
    query=Department.query.all()
    return render_template('department.html',query=query,user=current_user)

@app.route("/adddepartment",methods=['POST','GET'])
@login_required
def adddepartment():
    query=Department.query.all() 
    if request.method=='POST':
             
        depid=request.form.get('depid')
        depname=request.form.get('depname')
        department=Department(depid=depid,depname=depname)
        db.session.add(department)
        db.session.commit()
        
    return render_template('adddepartment.html',query=query,user=current_user)



@app.route("/ddelete/<string:id>",methods=['POST','GET'])
@login_required
def ddelete(id):
    dele=Department.query.filter_by(id=id).first()
    db.session.delete(dele)
    db.session.commit()
    flash("Date Deleted","danger")
    return redirect("/department")

@app.route("/addhospitaldata", methods=['GET', 'POST'])
def addhospitaldata():
    email=current_user.email
    posts=Hospitaluser.query.filter_by(email=email).first()
    code=posts.hcode
    postsdata=Hospital.query.filter_by(hcode=code).first()

    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        depid=request.form.get('depid')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubed')
        icubed=request.form.get('icubed')
        vbed=request.form.get('vbed')
        haddress=request.form.get('haddress')
        hcode=hcode.upper()
        huser=Hospitaluser.query.filter_by(hcode=hcode).first()
        hduser=Hospital.query.filter_by(hcode=hcode).first()
        if hduser:
            flash("Data is already Present you can update it..","primary")
            return render_template("hospitaldata.html")
        if huser:            
            new_data=Hospital(hcode=hcode,hname=hname,depid=depid,normalbed=normalbed,hicubed=hicubed,icubed=icubed,vbed=vbed,haddress=haddress)
            db.session.add(new_data)
            db.session.commit()

            return redirect('/addhospitaldata')
            

        else:
            flash("Hospital Code not Exist","warning")
            return redirect('/addhospitaldata')




    return render_template("hospitaldata2.html",user=current_user,postsdata=postsdata)

@app.route("/hoedit/<string:id>",methods=['POST','GET'])
@login_required
def hoedit(id):
    posts=Hospital.query.filter_by(id=id).first()
  
    if request.method=="POST":
        hcode=request.form.get('hcode')
        hname=request.form.get('hname')
        depid=request.form.get('depid')
        normalbed=request.form.get('normalbed')
        hicubed=request.form.get('hicubeds')
        icubed=request.form.get('icubeds')
        vbed=request.form.get('ventbeds')
        haddress=request.form.get('haddress')
        hcode=hcode.upper()
        update=Hospital.query.filter_by(id=id).first()
        update.hcode=hcode
        update.hname=hname
        update.depid=depid
        update.normalbed=normalbed
        update.hicubed=hicubed
        update.icubed=icubed
        update.vbed=vbed
        update.haddress=haddress
        db.session.commit()
        flash("Slot Updated","info")
        return redirect("/addhospitaldata")

    # posts=Hospitaldata.query.filter_by(id=id).first()
    return render_template("hoedit.html",posts=posts)

@app.route("/hodelete/<string:id>",methods=['POST','GET'])
@login_required
def hoodelete(id):
    dele=Hospital.query.filter_by(id=id).first()
    db.session.delete(dele)
    db.session.commit()
    flash("Date Deleted","danger")
    return redirect("/addhospitaldata")


@app.route("/hospital/<string:depid>",methods=['POST','GET'])

def hospitals(depid):
    query=Hospital.query.filter_by(depid=depid)
    return render_template('hospital.html',query=query,user=current_user)

@app.route("/bookbed",methods=['POST','GET'])
@login_required
def bookbed():
    query1=Hospital.query.all()
    query=Hospital.query.all()   
    if request.method=="POST":        
        srfid=request.form.get('srfid')
        bedtype=request.form.get('bedtype')
        hcode=request.form.get('hcode')
        spo2=request.form.get('spo2')
        pname=request.form.get('pname')
        pphone=request.form.get('pphone')
        paddress=request.form.get('paddress')  
        check2=Hospital.query.filter_by(hcode=hcode).first()
        checkpatient=Booking.query.filter_by(srfid=srfid).first()
        if checkpatient:
            flash("already srd id is registered ","warning")
            return render_template("booking.html",query=query,query1=query1)
        
        if not check2:
            flash("Hospital Code not exist","warning")
            return render_template("booking.html",query=query,query1=query1)

        code=hcode
        dbb=Hospital.query.filter_by(hcode=code).first()        
        bedtype=bedtype
        if bedtype=="NormalBed":       
            
                seat=dbb.normalbed
                print(seat)
                ar=Hospital.query.filter_by(hcode=code).first()
                ar.normalbed=seat-1
                db.session.commit()
                
            
        elif bedtype=="HICUBed":      
 
                seat=dbb.hicubed
                print(seat)
                ar=Hospital.query.filter_by(hcode=code).first()
                ar.hicubed=seat-1
                db.session.commit()

        elif bedtype=="ICUBed":     

                seat=dbb.icubed
                print(seat)
                ar=Hospital.query.filter_by(hcode=code).first()
                ar.icubed=seat-1
                db.session.commit()

        elif bedtype=="VENTILATORBed": 

                seat=dbb.vbed
                ar=Hospital.query.filter_by(hcode=code).first()
                ar.vbed=seat-1
                db.session.commit()
        else:
            pass

        check=Hospital.query.filter_by(hcode=hcode).first()
        if check!=None:
            if(seat>0 and check):
                res=Booking(srfid=srfid,bedtype=bedtype,hcode=hcode,spo2=spo2,pname=pname,pphone=pphone,paddress=paddress)
                db.session.add(res)
                db.session.commit()
                flash("Slot is Booked kindly Visit Hospital for Further Procedure","success")
                return render_template("booking.html",query=query,query1=query1)
            else:
                flash("Something Went Wrong","danger")
                return render_template("booking.html",query=query,query1=query1)
        else:
            flash("Give the proper hospital Code","info")
            return render_template("booking.html",query=query,query1=query1)
            
    
    return render_template("bedbooking.html",query=query,query1=query1,user=current_user)


@app.route("/padetails",methods=['GET'])
@login_required
def padetails():
    code=current_user.srfid
    print(code)
    data=Booking.query.filter_by(srfid=code).first()
    return render_template("padetails.html",data=data)

@app.route("/allpadetails",methods=['GET'])
@login_required
def allpadetails():
    code=current_user.hcode
    print(code)
    data=Booking.query.filter_by(hcode=code).first()
    return render_template("allpadetails.html",data=data)

@app.route("/alldepartment",methods=['POST','GET'])

def alldepartment():
    query=Department.query.all()
    return render_template('alldepartment.html',query=query,user=current_user)


@app.route("/allpdetails",methods=['GET'])
@login_required
def allpdetails():
    code=current_user.hcode
    print(code)
    data=Bookingpatient.query.filter_by(hcode=code)
    return render_template("allpdetails.html",data=data)

@app.route("/pharmacy",methods=['POST','GET'])
@login_required
def pharmacy():
    code=current_user.hcode
    query=Pharmacy.query.filter_by(hcode=code)
    return render_template('pharmacy.html',query=query,user=current_user)

@app.route("/addpharmacy",methods=['POST','GET'])
@login_required
def addpharmacy():
    code=current_user.hcode
    query=Pharmacy.query.filter_by(hcode=code)
    if request.method=='POST':
             
        phid=request.form.get('phid')
        phname=request.form.get('phname')
        department=Pharmacy(phid=phid,phname=phname,hcode=code)
        db.session.add(department)
        db.session.commit()
        
    return render_template('addpharmacy.html',query=query,user=current_user)

@app.route("/phdelete/<string:id>",methods=['POST','GET'])
@login_required
def phdelete(id):
    dele=Pharmacy.query.filter_by(id=id).first()
    db.session.delete(dele)
    db.session.commit()
    flash("Date Deleted","danger")
    return redirect("/addpharmacy")

@app.route("/about")
def about():
    return render_template('about.html',user=current_user)

@app.route("/contact")
def acontact():
    return render_template('contact.html',user=current_user)


if __name__=="__main__":
    app.run(debug=True)    
