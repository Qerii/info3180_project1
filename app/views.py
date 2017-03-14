"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import UserProfile
from werkzeug.utils import secure_filename
from forms import ProfileForm
import time
from datetime import *


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')



    
    
#adding a profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    file_folder = "app/static/uploads" 
    form = ProfileForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        user_age = request.form['age']
        user_gender = request.form['gender']
        user_info = request.form['bio']
        date_created = datetime.now()
        file = request.files['file']
        
        if file:    
            filename = secure_filename(file.filename)
            file.save(os.path.join(file_folder, filename))
            
            
            
            user = UserProfile(file=filename,username = username,first_name = first_name,last_name=last_name, age = user_age, gender= user_gender, biography = user_info, date_created = date_created) 
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('profile.html', form=form)
    
    
    
    
def timeinfo(entry):
    day = time.strftime("%a")
    date = time.strftime("%d")
    if (date <10):
        date = date.lstrip('0')
    month = time.strftime("%b")
    year = time.strftime("%Y")
    return day + ", " + date + " " + month + " " + year


@app.route('/profile/<userid>')
def viewProfile(userid):
    user = userProfile.query.filter_by(user_id = userid).first()
    image = '/static/uploads/' + user.img
    if request.method=='POST' or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json') and id!="":
        return jsonify(
            id=user.userid,
            image=user.file,
            username=user.username,
            firstname=user.first_name,
            lastname=user.last_name,
            gender=user.gender,
            age=user.age,
            bio=user.biography,   
            date=user.date_created)
    else:
        user = {'id':user.id,
        'image':image,
        'username':user.username,
        'firstname':user.firstname,
        'lastname':user.lastname,
        'age':user.age,
        'gender':user.gender,
        'bio':user.bio,
        'time':timeinfo(user.usertime)}
    return render_template('viewProfile.html', user=user)  








###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
