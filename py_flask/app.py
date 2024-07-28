from flask import Flask, render_template, request, redirect, url_for, session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random

smtp_server = 'smtp.gmail.com' # only gmails.
port = 587

sender_inf = "" # sender gmail.
sender_pass = "" # sender google application key.




app = Flask(__name__)
app.secret_key = '' # your secret key.

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process_data", methods=["POST"])
def process_data():
    login_name = request.form.get('l_name')
    login_pass = request.form.get('l_pass')
    loginInf = login_name + "|" + login_pass
    global VerfCode
    IntVerf = random.randint(8766,9852)
    VerfCode = f"#AXVAS-{IntVerf}"

    with open("login_information.txt", "r") as informationFile:
        for correctData in informationFile:
            if correctData.strip() == loginInf:
                IntVerf = random.randint(8766,9852)
                VerfCode = f"#AXVAS-{IntVerf}"

                msg = MIMEMultipart()
                msg['From'] = sender_inf
                msg['To'] = login_name
                msg['Subject'] = f'Your Verf Code -> {VerfCode}'
                body = 'FLASK TEST'
                msg.attach(MIMEText(body, 'plain'))
                try:

                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls()
                        server.login(sender_inf, sender_pass)
                        server.send_message(msg)
                    session["logged_in"] = True

                except smtplib.SMTPException as e:
                    print(e)
                    session["logged_in"] = False
                return redirect(url_for('threeFac'))

    session['logged_in'] = False
    return redirect(url_for('WrongLoginIndex'))

@app.route("/3Fac")
def threeFac():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template("3Fac.html")

@app.route("/WrongLogin")
def WrongLoginIndex():
    return render_template("WrongLoginIndex.html")

@app.route("/getVerf", methods=["POST"])
def process_verf():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    UserCode = request.form.get("usrcode")

    if UserCode.strip() == VerfCode:
        return render_template("Dashboard.html")
    else:
        session["logged_in"] = False
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
