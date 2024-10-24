from flask import Flask,request,render_template,redirect,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from scheduler import run_scheduled_task
import threading

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/FlaskDB'
mongo = PyMongo(app)
tasks_collection = mongo.db.task


@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index.html',tasks=tasks)

@app.route('/add',methods=['GET','POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        description = request.form['description']
        schedule_time = request.form['schedule_time']
        new_task = {
            "name":task_name,
            "description":description,
            "schedule_time":schedule_time,
            "status": "pending"
        }
        tasks_collection.insert_one(new_task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<task_id>',methods=['GET','POST'])
def edit_task(task_id):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if request.method == 'POST':
        updated_task = {
            "name": request.form['task_name'],
            "description": request.form['description'],
            "schedule_time": request.form['schedule_time'],
        }
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_task})
        return redirect(url_for('index'))
    return render_template('edit_task.html',task=task)


@app.route('/delete/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    threading.Thread(target=run_scheduled_task).start()
    app.run(debug=True,port=5001)
