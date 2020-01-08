from flask import render_template, redirect, url_for, request, g
from app import webapp
from flask import session

@webapp.route('/',methods=['GET'])
@webapp.route('/index',methods=['GET'])
@webapp.route('/main',methods=['GET'])
# Display an HTML page with links
def main():
    if "Authenticated" not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template("main.html",username=username)

