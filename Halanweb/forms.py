from flask_wtf import FlaskForm
from flask_login import current_user
from werkzeug.exceptions import LengthRequired
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField,SelectField, FloatField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField,FileAllowed
from Halanweb.models import User, Order
from dash_application.static_dicts import sme_name_list, Drivers_names_list


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



  # class SmeMainForm(FlaskForm):
  #     client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
  # order_id= StringField('order_id',validators=[DataRequired(),Length(7)])
  # client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
  # client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
  # sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
  # order_status=  SelectField('order_status',choices=['','Distibuted','Delivered','Hold','Cancelled'])
  # order_reason_of_failure= SelectField('order_reason_of_failure',choices=['','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
  # driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
  # order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
  # order_value= FloatField('order_value',validators=[DataRequired()])
  # order_date= DateField('order_date')
  # submit = SubmitField('Submit')

  # def validate_order_id(self, order_id):
  #     order = Order.query.filter_by(order_id=order_id.data).first()
  #     if order:
  #         raise ValidationError('That order ID already exists.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture=FileField("Update profile picture",validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    
    def validate_username(self, username):
         if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
   
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class UpdateorderForm(FlaskForm):
    client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
    order_id= StringField('order_id',validators=[DataRequired(),Length(7)])
    client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
    client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
    sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
    order_status=  SelectField('order_status',choices=['','Distibuted','Delivered','Hold','Cancelled'])
    order_reason_of_failure= SelectField('order_reason_of_failure',choices=['','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
    driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
    order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
    order_value= FloatField('order_value',validators=[DataRequired()])
    order_date= DateField('order_date')
    submit = SubmitField('Submit')

    def validate_order_id(self, order_id):
        order = Order.query.filter_by(order_id=order_id.data).first()
        if order:
            raise ValidationError('That order ID already exists.')


class orderForm(FlaskForm):
    client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
    order_id= StringField('order_id',validators=[DataRequired(),Length(7)])
    client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
    client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
    sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
    order_status=  SelectField('order_status',choices=['','Distibuted','Delivered','Hold','Cancelled'])
    order_reason_of_failure= SelectField('order_reason_of_failure',choices=['','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
    driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
    order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
    order_value= FloatField('order_value',validators=[DataRequired()])
    order_date= DateField('order_date')
    submit = SubmitField('Submit')

    def validate_order_id(self, order_id):
        order = Order.query.filter_by(order_id=order_id.data).first()
        if order:
            raise ValidationError('That order ID already exists.')

