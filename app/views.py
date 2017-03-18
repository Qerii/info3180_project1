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
    


@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    users = UserProfile.query.all()
    if users is not None:
        if request.method == 'POST':
            uList = []
            for user in users:
                uList.append({'Username':user.username, 'userid':user.userid})
            return jsonify(users=uList)
        flash('profiles found', 'success')
        return render_template('profiles.html', users = users)
    flash('No profile found', 'warning')
    return render_template('profiles.html')
    


@app.route('/profile/<userid>')
def user_profile(userid):
    user = UserProfile.query.filter_by( userid = userid).first()
    file = '/static/uploads/' + user.file
    if user is not None:
        if request.method == 'POST':
            uList = []
            for user in users:
                uList.append({'userid':user.userid,'Username':user.username, 'image': user.filename, 'gender':user.gender, 'age':user.age, 'profile_created_on':user.date_created })
            return jsonify(users=uList)
        flash('user found', 'success') 
        return render_template('user_profile.html', user = user, file=file)
    flash('No profile found', 'warning')
    return render_template('user_profile.html') 
        
    







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