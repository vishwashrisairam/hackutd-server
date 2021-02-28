
import os
import time
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


"""
postgres://roothack@tough-gecko-8mj.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=/home/oem/Desktop/utd/hackutd/backend/certs/ca.crt

"""

"""



@app.route('/api/users', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username)
    print(password)
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/<int:id>')
def get_user_details(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})
"""
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction


app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    def __init__(self,username):
        self.username= username

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        hash_pass = generate_password_hash(password)
        return self.password == hash_pass


@app.route('/test')
def hello():
    return jsonify({'message': 'Hello world'})

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    def check_user_exists(session):
        user = bool(session.query(User).filter_by(username=username).first())
        if user:
            abort(501,{'message':'Username already exists'})
    run_transaction(sessionmaker, check_user_exists)
    
    def callback(session):
        user = User(username=username)
        user.hash_password(password)
        session.add(user)      
    run_transaction(sessionmaker, callback)
    
    # db.session.commit()
    return (jsonify({'username': username,'message':'User created successfully'}), 201)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print('inside login')
    user = None 
    def callback(session):
        user = session.query(User).filter_by(username=username).one()
        if not user:  
            abort(501,{'message':'Username or password incorrect'})
        
        if not user.verify_password(password):
            print('ho')
            abort(501,{'message':'Username or password incorrect'})
        else: 
            return (jsonify({'username': username,'message':'Login successful'}), 200)

    run_transaction(sessionmaker, callback)

    




if __name__ == '__main__':
    # if not os.path.exists('db.sqlite'):
    #     db.create_all()
    app.run(debug=True)