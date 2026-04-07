import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mgk_key_123"

# ዳታቤዝ ግንኙነት
db_url = os.environ.get('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    try:
        reports = Report.query.order_by(Report.id.desc()).all()
    except:
        reports = [] # ዳታቤዙ ገና ካልተፈጠረ ባዶ ዝርዝር ያሳያል
    return render_template('index.html', reports=reports)

@app.route('/add', methods=['POST'])
def add():
    try:
        new_report = Report(
            date=request.form.get('date'),
            model=request.form.get('model'),
            serial_no=request.form.get('serial_no'),
            technician=request.form.get('technician'),
            activity=request.form.get('activity'),
            status=request.form.get('status'),
            remark=request.form.get('remark')
        )
        db.session.add(new_report)
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
