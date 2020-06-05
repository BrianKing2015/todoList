from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os
from datetime import datetime, timedelta

file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

db = SQLAlchemy(app)
# TODO write something to check for db and if none found run db.create_all(), so the models will work


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class EatIt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    yesterday = datetime.today() - timedelta(days=1)
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).filter(Todo.updated_on < (datetime.today() - yesterday)).all()
    return render_template('todo.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/eatit')
def eatit():
    one_week = datetime.today() + timedelta(days=7)
    food = EatIt.query.filter(EatIt.created_on < one_week).all()
    return render_template('eatit.html', food=food)


@app.route('/eatitadd', methods=['POST'])
def eatitadd():
    eatit = EatIt(text=request.form['eatititem'])
    db.session.add(eatit)
    db.session.commit()
    return redirect(url_for('eatit'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')