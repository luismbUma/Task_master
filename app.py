from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import os


app = Flask(__name__)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            try:
                mongo.db.todos.insert_one({
                    'content': task_content,
                    'completed': 0,
                    'date_created': datetime.utcnow()
                })
                return redirect(url_for('index'))
            except Exception as e:
                return f"Problem inserting value: {e}"
        else:
            return "Task content cannot be empty."
    else:
        try:
            tasks = list(mongo.db.todos.find().sort("date_created", 1))
            return render_template('index.html', tasks=tasks)
        except Exception as e:
            return f"Problem fetching tasks: {e}"
        

@app.route('/delete/<id>')
def delete(id):
    try:
        mongo.db.todos.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting the task.'

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    task = mongo.db.todos.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        new_content = request.form['content']
        try:
            mongo.db.todos.update_one(
                {'_id': ObjectId(id)},
                {'$set': {'content': new_content}}
            )
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)