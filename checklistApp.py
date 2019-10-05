from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist_db.sqlite3'
db = SQLAlchemy(app)

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    password = db.Column(db.String(256))

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)
    
@app.route('/')
def index():
    return render_template("index.html", title="Checklist")

@app.route('/checklist/<name>')
def checklist(name):
    if request.referrer == url_for("index",_external=True):
        return render_template("checklist.html", title="Checklist", name=name)
    else:
        abort(404)

@app.route("/setup", methods=["POST"])
def setup():
    checklist_name = request.form.get('name')
    # check here if name is already taken 
    if Checklist.query.filter_by(name=checklist_name).first():
        # TODO
        return f'Name already taken'
    # save credentails, hash password 
    else:
        checklist =  Checklist(name=checklist_name)
        checklist.set_password(request.form.get('password'))
        db.session.add(checklist)
        db.session.commit()
        return redirect(url_for("checklist", name=checklist_name))

@app.route("/search", methods=["POST"])
def search():
    search_text = request.form.get('search_text')
    valid_checklists = Checklist.query.filter(Checklist.name.startswith(search_text)).all()
    name_array = []
    for checklist in valid_checklists:
        name_array.append(checklist.name)
    return jsonify(names=name_array,names_length=len(name_array))

@app.route("/login", methods=["POST"])
def login():
    checklist_name = request.form.get('checklist_name')
    checklist = Checklist.query.filter_by(name=checklist_name).first()
    if checklist.check_password(request.form.get('password')):
        return redirect(url_for("checklist", name=checklist_name))
    else:
        # TODO
        return f'Wrong password'

if __name__ == '__main__':
    app.run(debug=True)