from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ለጊዜው መረጃው እዚህ ዝርዝር ውስጥ ይቀመጣል
activities = []

@app.route('/')
def home():
    return render_template('index.html', activities=activities)

@app.route('/add', methods=['POST'])
def add_activity():
    # ከፎርሙ መረጃውን መቀበል
    date = request.form.get('date')
    model = request.form.get('model')
    technician = request.form.get('technician')
    activity_desc = request.form.get('activity')
    status = request.form.get('status')
    
    # ወደ ዝርዝሩ መጨመር
    activities.append({
        'date': date,
        'model': model,
        'technician': technician,
        'activity': activity_desc,
        'status': status
    })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
