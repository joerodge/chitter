import os
from flask import Flask, request, redirect, render_template, session
from lib.database_connection import get_flask_database_connection
from lib.user import User, UserRepository
from lib.peep import Peep, PeepRepository
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key=''.join(random.choice('abcdefghi') for i in range(10))

@app.route('/')
def main_page():
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    user_repo = UserRepository(connection) 
    peeps = peep_repo.all()
    users = {}
    for peep in peeps:
        user = user_repo.get_user_by_id(peep.user_id)
        users[peep.id] = user.username
    return render_template('chitter.html', peeps=peeps[::-1], users=users)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    password_attempt = request.form['password']
    username = request.form['username'].strip().lower()
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    if user_repo.check_password(username, password_attempt):
        user = user_repo.get_user_by_username(username)
        session['user_id'] = user.id
        print(user.id)
        return render_template(f'user.html', just_logged_in=True, user=user)
    else:
        return render_template('login.html', errors='Login info was incorrect')

@app.route('/users/new', methods=['GET'])
def new_user():
    return render_template('new_user.html')


@app.route('/users/<id>', methods=['GET'])
def single_user(id):
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    user = user_repo.get_user_by_id(id)
    return render_template('user.html', user=user)


@app.route('/users', methods=['POST'])
def add_new_user():
    name = request.form['name'].strip()
    email = request.form['email'].strip().lower()
    username = request.form['username'].strip().lower()
    password = request.form['password']

    new_user = User(None, name, username, email, password)
    if not new_user.is_valid():
        return render_template('new_user.html', errors="Invalid entries")
    
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    errors = user_repo.check_user(new_user)
    if errors:
        return render_template('new_user.html', errors=', '.join(errors))
    else:
        new_id = user_repo.create_user(new_user)
        return redirect(f"/users/{new_id}")


@app.route('/peeps/new', methods=['GET'])
def new_peep():
    if 'user_id' not in session:
        return redirect('/login')
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    user = user_repo.get_user_by_id(session['user_id'])
    return render_template('new_peep.html', user=user)

@app.route('/peeps', methods=['POST'])
def create_new_peep():
    connection = get_flask_database_connection(app)
    peep_repo = PeepRepository(connection)
    user_repo = UserRepository(connection)
    content = request.form['content'].strip()
    timestamp = str(datetime.now())
    user = user_repo.get_user_by_id(session['user_id'])
    if not user:
        return render_template('new_peep.html', errors="User doesn't exist")
    
    peep = Peep(None, content, timestamp, user.id)
    peep_repo.create_new(peep)
    return redirect('/')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect('/')

    

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
