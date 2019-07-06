from flask import Flask, request, render_template
from flask_mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vinaykatare456@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/", methods=['POST'])
def index():
   if request.method == "POST":
       name = request.form["name"] 
       email_id = request.form["email"]
       msg = Message('Ant Hill Creations welcomes you!', sender = 'vinaykatare456@gmail.com', recipients = [email_id])
       link = "http://127.0.0.1:5000/survey.html"
       msg.body = "Hello "+name+" \n Ant Hill Creations welcomes you! Our motto is to aim at interactive learning environments in public spaces with a primary focus on sustainability. \n Thank you for registrating with us! \n To proceed with us, fill the survey in the survey link - " + link+ "From,\n Ant Hill Creations \n https://anthillcreations.org/"
       mail.send(msg)
       if request.form['confirm']:
            return render_template("http://127.0.0.1:5000/survey.html")
       return "Please check your email for the survey form."


       

if __name__ == '__main__':
   app.run(debug = True)