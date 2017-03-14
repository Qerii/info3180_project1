from flask_wtf import FlaskForm
#from flask_wtf.File import FileAllowed,FileField
from wtforms import StringField, PasswordField,RadioField,TextAreaField, IntegerField
from wtforms.validators import InputRequired


class ProfileForm(FlaskForm):
        image = StringField('Image', validators=[InputRequired()])
        firstname = StringField('Firstname', validators=[InputRequired()])
        lastname = StringField('Lastname', validators=[InputRequired()])
        username = StringField('Username', validators=[InputRequired()])
        age = IntegerField('Age', validators=[InputRequired()])
        gender = RadioField('Gender',choices=[('Male','Male'),('Female','Female')])
        bio = StringField('Bio', validators=[InputRequired()])
        
        

        


