from flask import Flask, render_template, request, redirect
from mongoengine import connect
from task import Task
import os, configparser

config = configparser.ConfigParser()
config.read('.env')

db = config.get('mongo', 'db', fallback='flask')
host = config.get('mongo', 'host', fallback='ds123084.mlab.com')
username = config.get('mongo', 'username', fallback='gjuniioor')
password = config.get('mongo', 'password', fallback='gjuniioor')
port = config.getint('mongo', 'port', fallback=23084)

connect(db=db, host=host, username=username, password=password, port=port)

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	tasks = Task.objects(complete=False, deleted=False)

	return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['POST'])
def create():
	title = request.form['title']
	priority = request.form['priority']
	duedate = request.form['duedate']

	task = Task(title=title, priority=priority, duedate=duedate, complete=False, deleted=False)
	task.save()

	return redirect('/')

@app.route('/delete/<id>')
def delete(id):
	Task.objects(pk=id).update_one(deleted=True)

	return redirect('/')

@app.route('/complete/<id>')
def complete(id):
	Task.objects(pk=id).update_one(complete=True)

	return redirect('/')

@app.route('/edit/<id>', methods=['POST'])
def edit(id):
	title = request.form['title']
	priority = request.form['priority']
	duedate = request.form['duedate']

	Task.objects(pk=id).update_one(title=title, priority=priority, duedate=duedate)

	return redirect('/')

if __name__ == '__main__':
	port = int(os.getenv('PORT',8080))
	host = os.getenv('IP', '0.0.0.0')
	app.run(port=port, host=host)