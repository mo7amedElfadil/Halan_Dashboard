from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Halanweb.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



 ###  class Sme_main(FlaskForm):
    ###client_contact_no= StringField('client_contact_no', varchar(10) NOT NULL,
       ### order_id= varchar(10) NOT NULL,
        ###client_city= varchar(150) NOT NULL,
        #client_address= varchar(150) NOT NULL, 
        #sme_name varchar=(150) NOT NULL,
        #order_status= varchar(150) NOT NULL,
        #order_reason_of_failure= varchar(255),
        #driver_name varchar(150)= NOT NULL,
    #order_delivery_fees= float(10) NOT NULL,
     #   order_value= float(10) NOT NULL,
      #  order_date= DATE NOT NULL"""
    