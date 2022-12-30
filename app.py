from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print(f"new Task: title = {request.form['title']}, description = {request.form['description']}")
        title = request.form['title']
        description = request.form['description']
        task = Task(title=title, description=description, status='Pending')
        db.session.add(task)
        db.session.commit() 
    # task = Task(title='Task 1', description='This is task 1', status='Pending')
    # db.session.add(task)
    # db.session.commit()
    allTasks = Task.query.all()
    print(allTasks)
    return render_template('index.html', allTasks=allTasks)
    # return 'Hello, World!'

# @ is a decorator in python it is used to add functionality to an existing code
@app.route('/show')
def show():
    allTasks = Task.query.all()
    print(allTasks)
    # return 'Show all tasks'
    # data = json.dumps(allTasks, default=vars)
    return "show all tasks"

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    updateTask = Task.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        print(f"Updating task: {updateTask}")
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.description = description
        task.status = status
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('hello_world'))
    return render_template('update.html', updateTask=updateTask)

@app.route('/delete/<int:sno>')
def delete(sno):
    task = db.get_or_404(Task, sno)
    print(f"Deleting task: {task}")
    db.session.delete(task)
    db.session.commit()
    return redirect('/')
    
    
if __name__ == '__main__':
    app.run(debug=True, port=6969)