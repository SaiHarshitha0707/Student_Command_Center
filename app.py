from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///study_tracker.db"
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

#Study-Tracker
class Study_Tracker(db.Model):
    subject = db.Column(db.String(200), primary_key=True, nullable=False)
    topic = db.Column(db.String(500), nullable=False)
    min = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/study_tracker', methods=['GET', 'POST'])
def study_tracker():
    if request.method == 'POST':
        subject = request.form['subject']
        topic = request.form['topic']
        min = request.form['min']

        study = Study_Tracker(subject = subject, topic=topic, min=min)
        db.session.add(study)
        db.session.commit()

    allStudy_Tracker = Study_Tracker.query.all()
    return render_template('study_tracker.html', allStudy_Tracker = allStudy_Tracker)

@app.route('/delete_study/<string:subject>/<string:topic>', methods=['GET', 'POST'])
def delete_study(subject, topic):
    study = Study_Tracker.query.filter_by(subject=subject, topic=topic).first()

    if study is None:
        return redirect('/study_tracker')
    
    db.session.delete(study)
    db.session.commit()
    return redirect('/study_tracker')


#Assignment-Tracker
class Assignment_Tracker(db.Model):
    subject = db.Column(db.String(200), primary_key=True, nullable=False)
    assignment = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Incomplete')

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/assignment_tracker', methods=['GET', 'POST'])
def assignment_tracker():
    if request.method == 'POST':
        sub = request.form['addSubject']
        name = request.form['addName']
        date_str = request.form['addDate']
        stat = request.form['addStatus']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        ass = Assignment_Tracker(subject=sub, assignment=name, date=date, status=stat)
        db.session.add(ass)
        db.session.commit()

    allAssignment_Tracker = Assignment_Tracker.query.all()
    return render_template('assignment_tracker.html', allAssignment_Tracker=allAssignment_Tracker)

@app.route('/assignment_tracker_completed')
def assignment_tracker_completed():
    assignments = Assignment_Tracker.query.filter_by(status='Completed').all()
    return render_template('assignment_tracker_completed.html', assignments=assignments)

@app.route('/assignment_tracker_pending')
def assignment_tracker_pending():
    assignments = Assignment_Tracker.query.filter_by(status='Incomplete').all()
    return render_template('assignment_tracker_completed.html', assignments=assignments)

@app.route('/update_ass/<string:subject>/<string:name>', methods=['GET', 'POST'])
def update_ass(subject, name):
    if request.method == 'POST':
            sub = request.form['updSubject']
            name = request.form['updName']
            date_str = request.form['updDate']
            stat = request.form['updStatus']
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
            ass = Assignment_Tracker.query.filter_by(subject=sub, assignment=name).first()
            ass.subject = sub
            ass.assignment = name
            ass.date = date
            ass.status = stat

            db.session.add(ass)
            db.session.commit()
            return redirect('/assignment_tracker')
    
    ass = Assignment_Tracker.query.filter_by(subject= subject, assignment=name).first() 
    return render_template('update_assignment.html', ass=ass)


@app.route('/delete_ass/<string:subject>/<string:name>')
def delete_ass(subject, name):
    ass = Assignment_Tracker.query.filter_by(subject=subject, assignment=name).first()

    if ass is None:
        return redirect('/assignment_tracker')
    
    db.session.delete(ass)
    db.session.commit()
    return redirect('/assignment_tracker')

#Expense-Tracker
class Expense_Tracker(db.Model):
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(200), primary_key=True, nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/expense_tracker', methods=['GET', 'POST'])
def expense_tracker():
    if request.method == 'POST':
        date_str = request.form['addDate']
        category = request.form['addCategory']
        desc = request.form['addDescription']
        amt = request.form['addAmount']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        expense = Expense_Tracker(date=date, category=category, desc=desc, amount=amt)
        db.session.add(expense)
        db.session.commit()

    allExpense = Expense_Tracker.query.all()
    return render_template('expense_tracker.html', allExpense=allExpense)

@app.route('/update_expense/<string:category>/<string:desc>', methods=['GET', 'POST'])
def update_expense(category, desc):
    if request.method == 'POST':
            date_str = request.form['updDate']
            category = request.form['updCategory']
            desc = request.form['updDesc']
            amount = request.form['updAmount']
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
            expense = Expense_Tracker.query.filter_by(category=category, desc=desc).first()
            expense.date = date
            expense.category = category
            expense.desc = desc
            expense.amount = amount

            db.session.add(expense)
            db.session.commit()
            return redirect('/expense_tracker')
    
    expense = Expense_Tracker.query.filter_by(category=category, desc=desc).first() 
    return render_template('update_expense.html', expense=expense)

@app.route('/delete_expense/<string:category>/<string:desc>')
def delete_expense(category, desc):
    expense = Expense_Tracker.query.filter_by(category=category, desc=desc).first()

    if expense is None:
        return redirect('/expense_tracker')
    
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expense_tracker')

@app.route('/statistics')
def statistics():
    allStudy = Study_Tracker.query.all()
    allAss = Assignment_Tracker.query.all()
    allExpense = Expense_Tracker.query.all()
    return render_template('statistics.html', allStudy=allStudy, allAss=allAss, allExpense=allExpense)

import urllib.request
import urllib.error
import json

@app.route('/weather_report', methods=['GET', 'POST'])
def weather_report():
    opp = []
    if request.method == 'POST':
        location = request.form.get('location')
        if not location:
            return "Missing location", 400
        print("DEBUG location:", repr(location))

        loc = urllib.parse.quote(location)
        url_1 =  "https://py4e-data.dr-chuck.net/opengeo?q=" + loc
        response_1 = urllib.request.urlopen(url_1)
        data_1 = response_1.read()
        data_1 = json.loads(data_1)

        if data_1["features"]:
            lon = data_1["features"][0]["properties"]["lon"]
            lat = data_1["features"][0]["properties"]["lat"]
        else:
            return "Location not found", 404

        url_2 = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&forecast_days=1&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,wind_direction_10m,precipitation&timezone=Asia%2FKolkata"
        response_2 = urllib.request.urlopen(url_2)
        data_2 = response_2.read()
        data_2 = json.loads(data_2)

        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",

            45: "Fog",
            48: "Depositing rime fog",

            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",

            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",

            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",

            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",

            95: "Thunderstorm"
        }
        op = [location, data_2["current"]["temperature_2m"], data_2["current"]["relative_humidity_2m"], data_2["current"]["wind_speed_10m"], data_2["current"]["wind_direction_10m"], data_2["current"]["precipitation"], weather_codes[data_2["current"]["weather_code"]]]
        opp = op
        return render_template('weather_report.html', op=op)
    
    return render_template('weather_report.html', op=opp)

@app.route('/github_repos')
def github_repos():
    return render_template('github_repos.html')

@app.route('/wikidata')
def wikidata():
    return render_template('wikidata.html')


if __name__ == '__main__':
    app.run(debug=True)