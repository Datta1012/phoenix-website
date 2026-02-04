from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

import os
import time

app = Flask(__name__)

# ==========================
# EMAIL CONFIGURATION
# ==========================

# -------- EMAIL CONFIGURATION (GMAIL) --------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dat.tambe1012@gmail.com'
app.config['MAIL_PASSWORD'] = 'nyrc hzdf hsdu olzb'

mail = Mail(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# EXISTING ROUTES (UNCHANGED)
# ==========================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/careers")
def careers():
    return render_template("careers.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/services/fire-detection')
def fire_detection():
    return render_template('fire_detection.html')

@app.route('/services/cctv')
def cctv_service():
    return render_template('cctv_service.html')

@app.route('/services/access-control')
def access_control():
    return render_template('access_control.html')

@app.route('/services/networking')
def networking():
    return render_template('networking.html')

@app.route('/services/it-infrastructure')
def it_infra():
    return render_template('it_infra.html')

@app.route('/services/computer-hardware')
def computer_hardware():
    return render_template('computer_hardware.html')

# ==========================
# CAREER & APPLY ROUTES
# ==========================

@app.route("/apply")
def apply():
    return render_template("apply.html")

@app.route("/submit_application", methods=["POST"])
def submit_application():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    position = request.form["position"] 
    resume = request.files["resume"]

    filename = secure_filename(resume.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    resume.save(filepath)

    msg = Message(
        subject="New Job Application",
        sender=email,
        recipients=["dat.tambe1012@gmail.com"]
    )

    msg.body = f"""
    New Job Application Received:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Applied For: {position}
    """

    # ✅ THIS LINE ATTACHES THE RESUME
    with app.open_resource(filepath) as fp:
        msg.attach(filename, "application/pdf", fp.read())

    mail.send(msg)

    return render_template("success.html")


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
