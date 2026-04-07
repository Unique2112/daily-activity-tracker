from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "any_secret_key"

# ዳታቤዝ ሊንኩን ማስተካከያ (Fix for Render)
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///reports.db'
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

@app.route('/')
def home():
    # ሁሉንም ሪፖርቶች ከዳታቤዝ አምጣ
    reports = Report.query.all()
    return render_template('index.html', reports=reports)

@app.route('/add', methods=['POST'])
def add_report():
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
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # ዳታቤዙን በራሱ ይፈጥራል
    app.run(debug=True)
