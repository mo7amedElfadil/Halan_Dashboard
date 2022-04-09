from flask_wtf import FlaskForm
from flask_login import current_user
from sqlalchemy import null, true
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
    role =  SelectField('Role',validators=[DataRequired()],
                                choices=['','Upper Management','Operations Manager','Drivers Supervisor','Data Entry Officer', 'Accountant','admin'])
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


class UploadForm(FlaskForm):
    csv_file =  FileField("Upload a CSV file",validators=[FileAllowed(['csv'])])
    submit = SubmitField('Upload')

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
 order_id= StringField('order_id',validators=[DataRequired(),Length(6)])
 client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
 client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
 client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
 sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
 order_value= FloatField('order_value',validators=[DataRequired()])
 order_date= DateField('order_date')
 driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
 order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
 order_reason_of_failure= SelectField('order_reason_of_failure',choices=['','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
 order_status=  SelectField('order_status',choices=['Distributed','Delivered','Hold','Cancelled'])
 submit = SubmitField('Submit')

class DeoOrderForm(FlaskForm):  
    order_id= StringField('order_id',validators=[DataRequired(),Length(6)])
    client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
    client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
    client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
    sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
    order_value= FloatField('order_value',validators=[DataRequired()])
    order_date= DateField('order_date')
    driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
    order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
    order_reason_of_failure= SelectField('order_reason_of_failure',choices=[' ','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
    order_status=  SelectField('order_status',choices=['Distributed','Delivered','Hold','Cancelled'])
    submit = SubmitField('Submit')  

class AccountantUpdateOrderForm (FlaskForm): 
 order_id= StringField('order_id',validators=[DataRequired(),Length(6)])
 client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
 client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
 client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
 sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
 order_value= FloatField('order_value',validators=[DataRequired()])
 order_date= DateField('order_date')
 driver_name= SelectField('driver_name',validators=[DataRequired(),],choices=Drivers_names_list)
 order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
 order_reason_of_failure= SelectField('order_reason_of_failure',choices=[' ','Requested to recieve another day','Wrong order info,Not answering','Fraud','Duplicate','Closed phone','Away'])
 order_status=  SelectField('order_status',choices=['Distributed','Delivered','Hold','Cancelled'])
 submit = SubmitField('Submit')  

class orderForm(FlaskForm):
 order_id= StringField('order_id',validators=[DataRequired(),Length(6)])
 client_contact_no= StringField('client_contact_no',validators=[DataRequired()])
 client_city= SelectField('client_city',validators=[DataRequired()],choices=['','Khartoum','Bahri','Omdurman'])
 client_address=StringField('client_address',validators=[DataRequired(),Length(min=5,max=150)])
 sme_name=SelectField('sme_name',validators=[DataRequired()],choices=sme_name_list)
 order_value= FloatField('order_value',validators=[DataRequired()])
 order_date= DateField('order_date')
 driver_name= SelectField('driver_name',validators=[DataRequired()],choices=Drivers_names_list)
 order_delivery_fees= FloatField('order_delivery_fees',validators=[DataRequired()])
 submit = SubmitField('Submit')

 def validate_order_id(self, order_id):
        order = Order.query.filter_by(order_id=order_id.data).first()
        if order:
            raise ValidationError('That order ID already exists.')

