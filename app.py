from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# ዳታቤዝ ማገናኛ (Render ላይ PostgreSQL ካለ እሱን ይጠቀማል)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///reports.db')
db = SQLAlchemy(app)

# የሪፖርት ሰንጠረዥ
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    model = db.Column(db.String(100))
    serial_no = db.Column(db.String(100))
    technician = db.Column(db.String(100))
    activity = db.Column(db.Text)
    status = db.Column(db.String(50))
    remark = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=0)

# ለሙከራ ዩዘሮች (በኋላ በዳታቤዝ መቀየር ይቻላል)
USERS = {
    "tech1": {"password": "123", "role": "technician"},
    "lead1": {"password": "123", "role": "supervisor"},
    "boss1": {"password": "123", "role": "manager"}
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    user = request.form.get('username')
    pwd = request.form.get('password')
    if user in USERS and USERS[user]['password'] == pwd:
        session['user'] = user
        session['role'] = USERS[user]['role']
        return redirect(url_for('dashboard'))
    return "ያልተፈቀደ ተጠቃሚ!"

@app.route('/dashboard')
def dashboard():
    reports = Report.query.all()
    return render_template('index.html', reports=reports, role=session.get('role'))

@app.route('/add', methods=['POST'])
def add_report():
    new_rep = Report(
        date=request.form.get('date'),
        model=request.form.get('model'),
        serial_no=request.form.get('serial_no'),
        technician=session.get('user'),
        activity=request.form.get('activity'),
        status=request.form.get('status'),
        remark=request.form.get('remark')
    )
    db.session.add(new_rep)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/approve/<int:id>')
def approve(id):
    rep = Report.query.get(id)
    rep.approved = True
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/rate/<int:id>', methods=['POST'])
def rate(id):
    rep = Report.query.get(id)
    rep.rating = request.form.get('rating')
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
