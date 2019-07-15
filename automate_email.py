from flask import Flask, request, render_template
from flask_mail import Mail, Message
from db import *

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/", methods=['POST'])
def register():
   if request.method == "POST":
       name = request.form["name"] 
       email_id = request.form["email"]
       if register_form(request.form["name"], request.form["email"], request.form["phone"], request.form["company"], request.form["company_name"], request.form["no_of_playgrounds"], request.form["location"], request.form["funding"], request.form["budget"], request.form["start_time"], request.form["preferences"]):
           msg = Message('Ant Hill Creations welcomes you!', sender = 'your_email', recipients = [email_id])
           link = "http://127.0.0.1:5000/survey.html"
           msg.body = "Hello "+name+" \n Ant Hill Creations welcomes you! Our motto is to aim at interactive learning environments in public spaces with a primary focus on sustainability. \n Thank you for registrating with us! \n To proceed with us, fill the survey in the survey link - " + link+ "\n From,\n Ant Hill Creations \n https://anthillcreations.org/"
           mail.send(msg)
           if request.form['confirm']:
                return render_template("http://127.0.0.1:5000/survey.html")
           return "Please check your email for the survey form."
       return "Registration has failed"

 
@app.route("/", methods=['POST'])
def survey():
   if request.method == "POST":
       email_id = request.form["email"]
       if survey_form(request.form["project_name"], request.form["field_type"], request.form["google_location"], request.form["address"], request.form["no_of_students"], request.form["min_age"], request.form["max_age"], request.form["snake_prone"], request.form["public_location"], request.form["vandalism_prone"], request.form["soil_condition"], request.form["play_elements"], request.form["underground_connections"], request.form["electric_posts"], request.form["trees"], request.form["rocks"], request.form["water_logging"], request.form["highway"], request.form["waterbodies"], request.form["disability"], request.form["maintainance_required"], request.form["additional_requirements"], request.form["email"]
):
           msg = Message('Survey form received and generic proposal attached.', sender = 'vinaykatare456@gmail.com', recipients = [email_id])   
           msg.body = "Hello, we have received your survey form and accordingly we have sent a generic proposal. Please find the attached generic proposal."
           with app.open_resource("proposal.ppt") as fp:
               msg.attach("proposal.ppt", "proposal.ppt", fp.read())
           mail.send(msg)
           return "Proposal will be sent to the email soon"
       return "Failure in filing survey form"
       

if __name__ == '__main__':
   app.run(debug = True)
