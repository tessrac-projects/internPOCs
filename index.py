# from crypt import methods
#from crypt import methods
from json import dumps
import flask
from flask_session import Session
import requests
from flask import jsonify, render_template,request,session,redirect
import random
import smtplib

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
app.config["USER_EMAIL"]= ""
Session(app)


global email_variable
email_varibale = ""

def generateOTP(otp_size = 6):
    final_otp = ''
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0,9))
    return final_otp

def sendEmailVerificationRequest(sender="interns753@gmail.com",receiver="yshivam9920@gmail.com", custom_text="Hello, Your OTP is "):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    google_app_password = "requwjxobnuvvxtq"
    server.login(sender,google_app_password)
    cur_otp = generateOTP()
    msg = custom_text +  cur_otp
    server.sendmail(sender,receiver,msg)
    server.quit()
    return cur_otp

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method=='GET'):
        if not session.get("Email"):
         return render_template('index.html')
        return redirect('/home') 
    if(request.method == 'POST'):
        data = request.form
        Email = data['Email']
        password = data['password']
        users = requests.post('http://127.0.0.1:5000/login',json={'Email':Email,'password':password})
        #print(users.status_code)
        if(users.status_code==500):
            return render_template('index.html',failed=True)
        global email_variable
        email_variable = Email
        session["Email"]=Email
        return redirect('/otplogin?verify=1')


@app.route('/register',methods=['GET','POST'])
def register():
     if(request.method=='GET'):
        if not session.get("Email"):
         return render_template('register.html')
        return redirect('/home') 
     if(request.method == 'POST'):
         data = request.form
         firstname = data['fname']
         middlename = data['mname']
         lastname = data['lname']  
         Email = data['Email']
         password = data['password']
         phonenumber = data['phone']
         address = ['address']
         confirmpassword = data['confirmpassword']
         if(password != confirmpassword):
            return render_template('register.html',passwordCheck=False)

         users = requests.post('http://127.0.0.1:5000/users/register',json={'firstname':firstname,'middlename':middlename,'lastname':lastname,'phonenumber':phonenumber,'address':address,'Email':Email,'password':password})
         #print(users.status_code)
         if(users.status_code==201):
              return redirect('/')
         return render_template('register.html',failed=True)

@app.route('/home',methods=['GET','POST'])
def dshboard():
    if(request.method=='GET'):
         return render_template('home.html')
    if(request.method == 'POST'): 
        session["Email"] = None
        return redirect("/")  

@app.route('/otplogin',methods=['GET','POST'])        
def otplogin():
    
    if (request.method == 'GET'):
        if(request.args.get('verify')=='1'):
            print(email_variable)
            current_otp = sendEmailVerificationRequest(receiver=email_variable) # this function sends otp to the receiver and also returns the same otp for our session storage
            session['current_otp'] = current_otp
            # session['Email'] = Email
            return redirect('/verify')  
        return render_template('otplogin.html')

    if (request.method == 'POST'):
        data = request.form
        Email = data['Email']
        print(Email)
        current_otp = sendEmailVerificationRequest(receiver=Email) # this function sends otp to the receiver and also returns the same otp for our session storage
        session['current_otp'] = current_otp
        session['Email'] = Email
        return redirect('/verify')     

@app.route('/verify',methods=['GET','POST'])     
def verify():
    if (request.method == 'POST'):
        current_user_otp = session['current_otp']
        print("Current User OTP",current_user_otp)
        user_otp = request.form['OTP'] 
        print("User OTP : ", user_otp)
     
        if int(current_user_otp) == int(user_otp): 
           Email=request.args.to_dict()
           session["Email"] = Email  
           return redirect('/dashboard')  
        else:
           return "<h3> Oops! Email Verification Failure, OTP does not match. </h3>"  

    return render_template('verify.html')
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if(request.method == 'POST'):
        session['Email'] = None
        return redirect('/')
    if(request.method == 'GET'):
        return render_template('home.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)
    app.secret_key = 'mysecret'
app.run()