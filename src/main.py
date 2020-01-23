from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
import numpy as np

# Use the application default credentials
project_id = 'ultimate-challenge'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

point_system = {
    'Bollsport': 12.7,
    'Cirkelträning': 12.0,
    'CrossFit': 13.0,
    'Cykling': 13.5,
    'Gym': 11.5,
    'Kampsport': 13.7,
    'Löpning': 13.9,
    'Racketsport': 12.2,
    'Simning': 10.1,
    'Yoga': 9.0,
    'Övrigt': 10.0}


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/leaderboard")
def leaderboard():

    # Get date function
    today = date.today()

    # Connect to firebase client
    db = firestore.client()

    # Get exercise stats
    users_ref = db.collection(u'exercise')
    docs = users_ref.stream()
    result = {}
    for doc in docs:
        name = doc.to_dict()['name']
        length_of_activity = doc.to_dict()['length_of_activity']
        points = doc.to_dict()['points']
        if name not in result:
            result[name] = [0, 0, 0, 0] # Activities, Length, Points, Activities/Day
        result[name][0] += 1
        result[name][1] += int(length_of_activity)
        result[name][2] += points

    for athlete in result:
        result[athlete][2] = round(result[athlete][2], 1)
        result[athlete][3] = result[athlete][0] / (today - date(2020, 1, 14)).days


    result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1][2], reverse=True)}

    return render_template("leaderboard.html", result=result)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Function for signing up a new athlete."""

    # Check for post method
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")

        # Connect to firebase
        db = firestore.client()

        # Add a new doc in collection 'user_info'
        user_data = {
            u'name': first_name,
            u'last_name': last_name,
            u'nickname': username}
        db.collection(u'user_info').document().set(user_data)

    # Render signup page
    return render_template("signup.html")

@app.route("/add_exercise", methods=['GET', 'POST'])
def add_exercise():

    # Get date function
    today = date.today()

    # Add minutes for point counter
    point_counter = [nr for nr in range(30, 185, 5)]

    # Connect to firebase client
    db = firestore.client()
    users_ref = db.collection(u'user_info')
    docs = users_ref.stream()
    user_names = []
    for doc in docs:
        user_names.append(doc.to_dict())

    # Check if it is a post method    
    if request.method == 'POST':
        date_value = request.form.get("date_value")
        athlete_name = request.form.get("athlete_name")
        activity_name = request.form.get("activity_name")
        activity_length = request.form.get("activity_length")

        # Check if all fields are filled out
        if 'Select' in [date_value, athlete_name, activity_name, activity_length]:
            return render_template("add_exercise.html", today=today, user_names=user_names, activities=point_system, point_counter=point_counter)

        points = np.log(int(activity_length) * point_system[activity_name])
        db = firestore.client()

        exercise_data = {
            u'date': date_value,
            u'name': athlete_name,
            u'activity': activity_name,
            u'length_of_activity': activity_length,
            u'points': points}

        # Add a new doc in collection 'exercise'
        db.collection(u'exercise').document().set(exercise_data)

        return render_template("add_exercise.html", success=True, activities=point_system, point_counter=point_counter, today=today, user_names=user_names)
    return render_template("add_exercise.html", activities=point_system, point_counter=point_counter, today=today, user_names=user_names)


@app.route("/stats", methods=['GET', 'POST'])
def stats():


    # Add minutes for point counter
    point_counter = [nr for nr in range(30, 185, 5)]

    # Check if it is a post method
    if request.method == 'POST':
        activity_name = request.form.get("activity_name")
        activity_length = request.form.get("activity_length")

        # Caluculate points
        points = np.log(int(activity_length) * point_system[activity_name])
        return render_template("stats.html", activities=point_system, point_counter=point_counter, points=round(points, 1), activity_name=activity_name, activity_length=activity_length, box=True)


    return render_template("stats.html", activities=point_system, point_counter=point_counter, box=False)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
