from flask import Flask, render_template, request, url_for, abort, session, redirect
from flask_mail import Mail, Message
from db import *
import pandas as pd
import img2pdf 
from PIL import Image 
import os 
from PyPDF2 import PdfFileMerger  

app = Flask(__name__)
app.secret_key = ''

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vinaykatare456@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/request', methods=['POST', 'GET'])
def ask_request():
    if request.method == "POST":
        name = request.form["name"] 
        to_email = request.form["email"]
        print(request.form)
        if request_form(request.form["name"], request.form["email"], request.form["phone"], request.form["company"], request.form["company_name"], request.form["no_of_playgrounds"], request.form["location"], request.form["funding"], request.form["budget"], request.form["start_time"], request.form["preferences"]):
            msg = Message('Ant Hill Creations welcomes you!', sender = 'vinaykatare456@gmail.com', recipients = [to_email])
            link = "http://127.0.0.1:5000/survey.html"
            msg.body = "Hello "+name+" \n Ant Hill Creations welcomes you! Our motto is to aim at interactive learning environments in public spaces with a primary focus on sustainability. \n Thank you for registrating with us! \n To proceed with us, fill the survey in the survey link - " + link+ "\n Regards,\n Ant Hill Creations \n https://anthillcreations.org/"
            with app.open_resource('static/pdfs/brochure.pptx') as fp:
                msg.attach(filename='static/pdfs/brochure.pptx', data=fp.read(), content_type="application/pdf")
            mail.send(msg)
            return redirect(url_for('confirm_for_survey'))
        abort(500)
    return render_template('register.html')


@app.route('/do_survey')
def confirm_for_survey():
   return render_template('confirm.html')


@app.route("/survey", methods=['POST', 'GET'])
def survey():
    if request.method == "POST":
        to_email = request.form["email"]
        if survey_form(request.form["project_name"], request.form["field_type"], request.form["google_location"], request.form["address"], request.form["no_of_students"], request.form["age"], request.form["area"], request.form["snake_prone"], request.form["public_location"], request.form["vandalism_prone"], request.form["soil_condition"], request.form["play_elements"], request.form["underground_connections"], request.form["electric_posts"], request.form["trees"], request.form["rocks"], request.form["water_logging"], request.form["highway"], request.form["waterbodies"], request.form["disability"], request.form["maintainance_required"], request.form["additional_requirements"], request.form["email"]
):
            msg = Message('Survey form received and generic proposal attached.', sender = 'vinaykatare456@gmail.com', recipients = [to_email])   
            msg.body = "Hello, we have received your survey form and accordingly we have sent a generic proposal. Please find the attached generic proposal."
            result = request_by_email(request.form["email"])
            # print(result[0][33]) 
            result_file = get_ppt(result[0][33], request.form["area"], request.form["snake_prone"], request.form["disability"], result[0][0])
            if result_file == '':
                abort(500)
            with app.open_resource(result_file) as fp:
                msg.attach(filename=result_file, data=fp.read(), content_type="application/pdf")
            mail.send(msg)
            return redirect(url_for('survey_done'))
        abort(500)
    return render_template('survey.html')


@app.route('/surveydone')
def survey_done():
   return render_template('survey_done.html')


@app.route('/dashboard/admin')
def dashboard_admin():
    if session.get('login'):
        stream=request_list()
        return render_template('admindash.html', stream=stream)
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/admin/<user_id>')
def dashboard_admin_user_info(user_id):
    if session.get('login'):
        user=request_by_id(user_id)
        print(user)
        return render_template('details.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/admin/<user_id>/start')
def dashboard_admin_user_pic(user_id):
    if session.get('login'):
        # user=request_list_by_id(user_id)
        return render_template('pic.html')
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/<user_id>')
def dashboard_user(user_id):
    if session.get('login'):
        user = request_by_id(user_id)
        return render_template('userdash.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == "admin@admin.com" and "admin"== password:
            session['login'] = True
            session['user_id'] = 0
            return redirect(url_for('dashboard_admin'))    
        result = login_user(email, password)
        if result:
            session['login'] = True
            session['user_id'] = result[0]
            return redirect(url_for('dashboard_user', user_id=result[0]))    
    return render_template('login.html')


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def server_error(error):
    return render_template('404.html'), 404


def printknapSack(W, wt, val, n, mval): 
    K = [[0 for w in range(W + 1)] for i in range(n + 1)] 

    for i in range(n + 1): 
        for w in range(W + 1): 
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w and max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]):
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]) 
            else: 
                K[i][w] = K[i - 1][w] 


    res = K[n][W] 
    
    w = W
    ans=set()
    for i in range(n, 0, -1): 
        if res <= 0: 
            continue
        if res == K[i - 1][w]: 
            continue
        elif mval-val[i-1] >=0:
            ans.add(i-1) 
            res = res - val[i - 1] 
            mval=mval-val[i-1]
            w = w - wt[i - 1] 
            #print(mval,w)
    print(ans)
    return ans


# Driver program to test above function 
def get_ppt(budget, area, snake_prone, disabled, user_id):
    snake_prone = 1 if (snake_prone == "Yes") else 0
    disabled = 1 if (disabled == "Yes") else 0
    print(budget, area, snake_prone, disabled)
    df = pd.read_csv("static/anthill.csv")
    print(df.head())
    df["A"] = df["Area"] + (df["Excess"]*df["Area"])/100
    val = []
    wt = []
    data={
        "Budget" : budget,
        "Area" : area,
        "snake" : snake_prone,
        "disabled" : disabled
    }
    k=0
    store=dict()
    for (a,b,c,d,e) in zip(df["A"],df["Budget"],df["Snake"],df["Disabled"],df["Product"]):
        if c==data["snake"] and d==data["disabled"]:
            val.append(a)
            wt.append(b)
            store[k]=e
            k=k+1
       
    W = int(data["Budget"][-6:])
    print(W)
    mval = int(data["Area"])
    n = len(val) 
    res=printknapSack(W, wt, val, n,mval)
    merger = PdfFileMerger()
    y = list(res)
    # print(res)
    if not res:
        return ''
    for i in y:
        # storing image path 
        img_path = "static/images/"+str(i)+".jpg"
        
        # storing pdf path 
        pdf_path = "static/pdfs/"+str(i)+".pdf"
          
        # opening image 
        image = Image.open(img_path) 
        print(image)
        # converting into chunks using img2pdf 
        pdf_bytes = img2pdf.convert(image.filename) 
        print(pdf_bytes)
        # opening or creating pdf file 
        file = open(pdf_path, "wb") 
        
        # writing pdf files with chunks 
        file.write(pdf_bytes)
        merger.append(pdf_path)
          
        # closing image file 
        image.close() 
          
        # closing pdf file 
        file.close() 
          
    # output 
    result_file = "static/pdfs/result"+str(user_id)+".pdf"
    merger.write(result_file)
    merger.close()
    return result_file

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
