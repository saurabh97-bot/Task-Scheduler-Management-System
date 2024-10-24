import schedule
import time
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


client = MongoClient('mongodb://localhost:27017/')
db = client['FlaskDB']
tasks_collection = db['task1']

def run_scheduled_task():
    while True:
        schedule.run_pending()
        time.sleep(1)

def execute_task(task_id):
    task = tasks_collection.find_one({"_id":ObjectId(task_id)})
    if task:
        print(f"Executing task: {task['name']}")
        tasks_collection.update_one({"_id":ObjectId(task_id)})


def schedule_tasks():
    tasks = tasks_collection.find()
    for task in tasks:
        schedule_time = task['schedule_time']
        schedule.every().day.at(schedule_time).do(execute_task,task_id=task['_id'])

schedule_tasks()