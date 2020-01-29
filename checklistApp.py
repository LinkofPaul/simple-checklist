from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist_db.sqlite3'
db = SQLAlchemy(app)

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='checklist', lazy=True)

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    #tmp solution
    name_non_white = db.Column(db.String(75), nullable=False)
    done = db.Column(db.Boolean)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.id'))

@app.route('/')
def index():
    return render_template("index.html", title="Simple Checklist")

@app.route('/checklist/<name>')
def checklist(name):
    if not request.referrer:
        abort(404)
    else:
        # load all tasks form Checklist(name) into variable tasks
        checklist = Checklist.query.filter_by(name=name).first()
        tasks = checklist.tasks
        return render_template("checklist.html", title="%s - Checklist" %(name), name=name, tasks=tasks)

def append_task(checklist_name, task_name):
    checklist = Checklist.query.filter_by(name=checklist_name).first()
    task = Task(name=task_name, name_non_white=task_name.replace(" ", ""), done=False)
    checklist.tasks.append(task)
    db.session.add(checklist)
    db.session.add(task)
    db.session.commit()
    
def reload_checklist(checklist_name):
    checklist = Checklist.query.filter_by(name=checklist_name).first()
    tasks = checklist.tasks
    return render_template("checklist.html", title="%s - Checklist" %(checklist_name), name=checklist_name, tasks=tasks)

@app.route('/checklist/add_task', methods=["POST"])
def add_task():
    checklist_name = request.form.get('name')
    task_name = request.form.get('newTask')
    append_task(checklist_name, task_name)
    return reload_checklist(checklist_name)

@app.route('/checklist/process_task', methods=["POST"])
def process_task():
    checklist_name = request.form.get('checklist_name')
    task_name = request.form.get('task_name')
    #check_button = request.form.get('check_button')
    task_remove_button = request.form.get('task_remove_button')
    if task_remove_button != None:
        checklist = Checklist.query.filter_by(name=checklist_name).first()
        tasks = checklist.tasks
        #TODO somehow last task in list can not be removed
        for task in tasks:
            if task.name == task_name:
                db.session.delete(task)
        db.session.add(checklist)
        db.session.add(task)
        db.session.commit()
        return reload_checklist(checklist_name)
    else:
        checklist = Checklist.query.filter_by(name=checklist_name).first()
        tasks = checklist.tasks
        for task in tasks:
            if task.name == task_name:
                task.done = not task.done
        db.session.add(checklist)
        db.session.add(task)
        db.session.commit()
        return reload_checklist(checklist_name)

@app.route("/setup", methods=["POST"])
def setup():
    checklist_name = request.form.get('name').strip()
    # check here if name is already taken 
    if Checklist.query.filter_by(name=checklist_name).first():
        return jsonify(error=True)
    # save credentails, hash password 
    else:
        checklist =  Checklist(name=checklist_name)
        checklist.set_password(request.form.get('password'))
        db.session.add(checklist)
        db.session.commit()
        return jsonify(error=False, redirectURL=url_for("checklist", name=checklist_name, _external=True))

@app.route("/search", methods=["POST"])
def search():
    search_text = request.form.get('search_text')
    if search_text == "":
        return jsonify(names=[], names_length=0)
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
        return jsonify(error=False, redirectURL=url_for("checklist", name=checklist_name, _external=True))
    else:
        return jsonify(error=True)

if __name__ == '__main__':
    app.run(debug=True)