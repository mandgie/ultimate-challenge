from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
project_id = 'ultimate-challenge'
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/leaderboard")
def leaderboard():
    db = firestore.client()
    users_ref = db.collection(u'exercise')
    docs = users_ref.stream()
    print('Hello world')
    doc_list = []
    for doc in docs:
        doc_list.append(doc.to_dict())
    return render_template("leaderboard.html", doc_list=doc_list)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_new")
def login_new():
    return render_template("login_new.html")

@app.route("/add_exercise", methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        date_value = request.form.get("date_value")
        athlete_name = request.form.get("athlete_name")
        activity_name = request.form.get("activity_name")
        activity_length = request.form.get("activity_length")
    return render_template("add_exercise.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")
    
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
