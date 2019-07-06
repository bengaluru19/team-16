from flask import Flask, render_template, request, url_for, abort, session
from flask_mail import Mail, Message
from db import *

app = Flask(__name__)
app.secret_key = ''

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vinaykatare456@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/request', methods=['POST'])
def ask_request():
    if request.method == "POST":
        name = request.form["name"] 
        to_email = request.form["email"]
        if register_form(request.form["name"], request.form["email"], request.form["phone"], request.form["company"], request.form["company_name"], request.form["no_of_playgrounds"], request.form["location"], request.form["funding"], request.form["budget"], request.form["start_time"], request.form["preferences"]):
            msg = Message('Ant Hill Creations welcomes you!', sender = 'vinaykatare456@gmail.com', recipients = [to_email])
            link = "http://127.0.0.1:5000/survey.html"
            msg.body = "Hello "+name+" \n Ant Hill Creations welcomes you! Our motto is to aim at interactive learning environments in public spaces with a primary focus on sustainability. \n Thank you for registrating with us! \n To proceed with us, fill the survey in the survey link - " + link+ "\n Regards,\n Ant Hill Creations \n https://anthillcreations.org/"
            mail.send(msg)
            return redirect(url_for('confirm_for_survey'))
        abort(500)
    return render_template('register.html')


@app.route('/do_survey')
def confirm_for_survey():
   return render_template('confiem.html')


@app.route("/survey", methods=['POST'])
def survey():
    if request.method == "POST":
        to_email = request.form["email"]
        if survey_form(request.form["project_name"], request.form["field_type"], request.form["google_location"], request.form["address"], request.form["no_of_students"], request.form["min_age"], request.form["max_age"], request.form["snake_prone"], request.form["public_location"], request.form["vandalism_prone"], request.form["soil_condition"], request.form["play_elements"], request.form["underground_connections"], request.form["electric_posts"], request.form["trees"], request.form["rocks"], request.form["water_logging"], request.form["highway"], request.form["waterbodies"], request.form["disability"], request.form["maintainance_required"], request.form["additional_requirements"], request.form["email"]
):
            msg = Message('Survey form received and generic proposal attached.', sender = 'vinaykatare456@gmail.com', recipients = [email_id])   
            msg.body = "Hello, we have received your survey form and accordingly we have sent a generic proposal. Please find the attached generic proposal."
            with app.open_resource("proposal.ppt") as fp:
                msg.attach("proposal.ppt", "proposal.ppt", fp.read())
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
        user=request_list_by_id(user_id)
        return render_template('projectforadmin.html', user=user, image=image)
    else:
        return redirect(url_for('login'))


@app.route('/dashboard/<user_id>')
def dashboard_user(user_id):
    if session.get('login'):
        user = request_by_id(user_id)
        return render_template('userdash.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == "admin@admin.com" and check_password_hash("admin", password):
            return redirect(url_for('dashboard_admin'))    
        result = login_user(email, password)
        if result:
            return redirect(url_for('dashboard_user', user_id=result[0]))    
    return render_template('login.html')


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def server_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
