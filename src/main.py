from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date

today = date.today()

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

point_counter = [nr for nr in range(30, 185, 5)]



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/leaderboard")
def leaderboard():
    # Connect to firebase client
    db = firestore.client()
    users_ref = db.collection(u'exercise')
    docs = users_ref.stream()
    doc_list = []
    for doc in docs:
        doc_list.append(doc.to_dict())
    point_counter = [nr for nr in range(30, 185, 5)]
    return render_template("leaderboard.html", doc_list=doc_list)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")

        # Connect to firebase
        db = firestore.client()

        user_data = {
            u'name': first_name,
            u'last_name': last_name,
            u'nickname': username}

        # Add a new doc in collection 'user_info' 
        db.collection(u'user_info').document().set(user_data)

    return render_template("signup.html")

@app.route("/add_exercise", methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        date_value = request.form.get("date_value")
        athlete_name = request.form.get("athlete_name")
        activity_name = request.form.get("activity_name")
        activity_length = request.form.get("activity_length")

        db = firestore.client()

        exercise_data = {
            u'date': date_value,
            u'name': athlete_name,
            u'activity': activity_name,
            u'length_of_activity': activity_length}

        # Add a new doc in collection 'exercise'
        db.collection(u'exercise').document().set(exercise_data)

    # Connect to firebase client
    db = firestore.client()
    users_ref = db.collection(u'user_info')
    docs = users_ref.stream()
    user_names = []
    for doc in docs:
        user_names.append(doc.to_dict())
        
    return render_template("add_exercise.html", activities=point_system, point_counter=point_counter, today=today, user_names=user_names)

@app.route("/stats")
def stats():
    return render_template("stats.html")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
