__author__ = 'wilsonincs'

from flask import Flask, render_template
from flask import request,redirect,url_for
import re
import pickle
import os.path
app = Flask(__name__)

loaded = False
err_msg = ''

if os.path.isfile('todolist.pkl'):
    pkl = open('todolist.pkl','rb')
    todo = pickle.load(pkl)
    pkl.close()
    loaded = True
else:
    todo = []

@app.route('/')
def print_list():
    return render_template('index.html',todo=todo,err_msg=err_msg)

@app.route('/submit', methods = ['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    if re.search(r'@\w*\.\w',email):
        if priority in ('high','medium','low'):
            todo.append(task + ' for ' + email + '. Priority: ' + priority)
        else:
            err_msg = 'Please select a priority level'
    else:
        err_msg = 'Please enter a valid e-mail'
    return redirect(url_for('print_list'))

@app.route('/clear', methods = ['POST'])
def clear():
    del todo[:]
    return redirect(url_for('print_list'))

@app.route('/write', methods = ['POST'])
def write():
    if loaded:
        fh = open('todolist.pkl','ab')
    else:
        fh = open('todolist.pkl','wb')
    pickle.dump(todo,fh)
    fh.close()
    return redirect(url_for('print_list'))



if __name__ == '__main__':
    app.debug = True
    app.run()