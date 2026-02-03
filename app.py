from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# ==========================
# EMAIL CONFIGURATION
# ==========================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# 👉 IMPORTANT — replace with YOUR Gmail + App Password
app.config['MAIL_USERNAME'] = 'yourgmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'

mail = Mail(app)

# Folder to store uploaded resumes
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    position = request.form['position']
    resume = request.files['resume']

    # Save resume
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(resume_path)

    # Prepare email
    msg = Message(
        subject=f"New Job Application - {position}",
        sender=app.config['MAIL_USERNAME'],
        recipients=["phoenixtechnico@gmail.com"]
    )

    msg.body = f"""
    New Job Application Received:

    Name: {name}
    Phone: {phone}
    Email: {email}
    Position Applied: {position}
    """

    # Attach resume
    with app.open_resource(resume_path) as fp:
        msg.attach(resume.filename, "application/pdf", fp.read())

    mail.send(msg)

    return render_template("success.html")

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
