from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist_db.sqlite3'
db = SQLAlchemy(app)

class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='checklist', lazy=True)

    def set_password(self, password):
        self.password = sha256_crypt.hash(password)

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.id'))

    def create_index(self):
        self.index = "task" + str(self.id)

@app.route('/')
def index():
    return render_template("index.html", title="Simple Checklist")

def status_Checklist(tasks):
    percentage = 0
    tasks_done = 0
    for task in tasks:
        if task.done:
            tasks_done += 1
    if len(tasks) > 0:
        percentage = int(tasks_done / len(tasks) * 100)
    return str(percentage) + "%"

@app.route('/checklist/<name>')
def checklist(name):
    if not request.referrer:
        abort(403)
    else:
        # load all tasks form Checklist(name) into variable tasks
        checklist = Checklist.query.filter_by(name=name).first()
        tasks = checklist.tasks
        percentage = status_Checklist(checklist.tasks)
        return render_template("checklist.html", title="%s - Checklist" %(name), name=name, tasks=tasks, percentage=percentage, percent_num=percentage[ :-1])

@app.route('/checklist/add_task', methods=["POST"])
def add_task():
    checklist_name = request.form.get('name')
    task_name = request.form.get('newTask').strip()
    checklist = Checklist.query.filter_by(name=checklist_name).first()
    # check if Task has already been added
    task_taken = False
    for task in checklist.tasks:
        if task_name == task.name:
            task_taken = True
    if task_taken:
        return jsonify(error=True)
    else:
        task = Task(name=task_name, done=False)
        checklist.tasks.append(task)
        db.session.add(checklist)
        db.session.add(task)
        db.session.commit()
        # double commit of new task to add custom index using the id of object
        task.create_index()
        db.session.add(checklist)
        db.session.add(task)
        db.session.commit()
        return jsonify(error=False, redirectURL=url_for("checklist", name=checklist_name, _external=True))

@app.route('/checklist/process_task', methods=["POST"])
def process_task():
    checklist_name = request.form.get('checklist_name')
    task_name = request.form.get('task_name')
    task_remove_button = request.form.get('task_remove_button')
    if task_remove_button != None:
        checklist = Checklist.query.filter_by(name=checklist_name).first()
        tasks = checklist.tasks
        db.session.add(checklist)
        for task in tasks:
            if task.name == task_name:
                db.session.delete(task)
        db.session.commit()
        return redirect(url_for("checklist", name=checklist_name, _external=True))
    else:
        checklist = Checklist.query.filter_by(name=checklist_name).first()
        tasks = checklist.tasks
        db.session.add(checklist)
        for task in tasks:
            if task.name == task_name:
                task.done = not task.done
                db.session.add(task)
        db.session.commit()
        return redirect(url_for("checklist", name=checklist_name, _external=True))

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
    name_concat_array = []
    for name in name_array:
        name_concat_array.append(name.replace(" ", ""))
    return jsonify(names=name_array, names_concat=name_concat_array, names_length=len(name_array))

@app.route("/login", methods=["POST"])
def login():
    checklist_name = request.form.get('checklist_name')
    checklist = Checklist.query.filter_by(name=checklist_name).first()
    if checklist.check_password(request.form.get('password')):
        return jsonify(error=False, redirectURL=url_for("checklist", name=checklist_name, _external=True))
    else:
        return jsonify(error=True)

if __name__ == '__main__':
    db.create_all()
    app.run()