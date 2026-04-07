import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mgk_super_secret_key"

# ዳታቤዝ ግንኙነት
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///tech_report.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    approved = db.Column(db.Boolean, default=False) # የማጽደቂያ ቦታ

# ተጠቃሚዎች
USERS = {
    "tech1": "123", # ሪፖርት ብቻ የሚሞላ
    "lead1": "123", # ሪፖርት የሚሞላና Approve የሚያደርግ
    "boss1": "123"  # ሁሉንም የሚያይና Approve የሚያደርግ
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    user = request.form.get('username')
    pwd = request.form.get('password')
    if USERS.get(user) == pwd:
        session['user'] = user
        return redirect(url_for('dashboard'))
    return "የተሳሳተ መረጃ! እባክዎ ድጋሚ ይሞክሩ።"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    
    reports = Report.query.order_by(Report.id.desc()).all()
    return render_template('index.html', reports=reports, username=session['user'])

@app.route('/add', methods=['POST'])
def add():
    new_rep = Report(
        date=request.form.get('date'),
        model=request.form.get('model'),
        serial_no=request.form.get('serial_no'),
        technician=request.form.get('technician'),
        activity=request.form.get('activity'),
        status=request.form.get('status'),
        remark=request.form.get('remark')
    )
    db.session.add(new_rep)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/approve/<int:id>')
def approve(id):
    if session.get('user') in ['lead1', 'boss1']:
        report = Report.query.get(id)
        report.approved = True
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
