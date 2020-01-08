from flask import Flask, render_template, request, redirect, url_for, session, Response
from app import webapp
from .utils import check_name, save_reg, check_password
from flask import jsonify


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'Authenticated' in session:
        return redirect(url_for('main'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #check username validated or not.
        if not check_name(request.form['username']):
            msg = 'Invalid Username'
            return render_template('login.html', msg=msg)

        account = check_password(request.form['username'],request.form['password'])
        if account:
            # Create session data, we can access this data in other routes
            session['Authenticated'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('main'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@webapp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('Authenticated', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

    

@webapp.route('/register', methods=['GET', 'POST'])
def register():
    rules = [lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
             lambda s: any(x.islower() for x in s),  # must have at least one lowercase
             lambda s: any(x.isdigit() for x in s),  # must have at least one digit
             lambda s: len(s) >= 7, # must be at least 7 characters
             lambda s: len(s) <= 17  # must be at most 16 characters
             ]
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'repassword' in request.form:
        if request.form['password'] != request.form['repassword']:
            msg = 'Password and Repeated Password Should Be the Same!'
            return render_template('register.html', msg=msg)
        # check the availability of username
        if check_name(request.form['username']) is not None:
            msg = 'Choose Another Cool Username Please!'
            return render_template('register.html', msg=msg)
        if len(request.form['username']) > 30:
            msg = 'Username is too long!'
            return render_template('register.html', msg=msg)
        if not all(rule(request.form['password']) for rule in rules):
            msg = 'Password is Not Accepted!'
        else:
            username = request.form['username']
            password = request.form['password']
            msg = save_reg(username,password)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@webapp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@webapp.route('/api/register', methods=['GET'])
def script():
    return render_template("api_register.html")
#API:
@webapp.route('/api/register', methods=['POST'])
def api_register():
    rules = [lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
             lambda s: any(x.islower() for x in s),  # must have at least one lowercase
             lambda s: any(x.isdigit() for x in s),  # must have at least one digit
             lambda s: len(s) >= 7,  # must be at least 7 characters
             lambda s: len(s) <= 17  # must be at most 7 characters
             ]
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # check the availability of username
        if check_name(request.form['username']) is not None:
            msg = 'Choose Another Cool Username Please!'
            return jsonify(status='register-error', msg = msg,state = 406)
        if len(request.form['username']) > 30:
            msg = 'Username is too long!'
            return jsonify(status='register-error', msg = msg, state = 406)
        if not all(rule(request.form['password']) for rule in rules):
            msg = 'Password is not Accepted!'
            return jsonify(status='register-error', msg = msg, state = 406)
        else:
            username = request.form['username']
            password = request.form['password']
            save_reg(username,password)
            msg = 'Successful Registered'
            return jsonify(status='Accepted', msg = msg, state = 200)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return jsonify(status='register-error',msg = msg, state = 406)