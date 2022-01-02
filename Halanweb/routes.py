
import flask
from PIL import Image
import secrets
import os
from flask import render_template, url_for, flash, redirect, request,abort
from Halanweb import db, bcrypt, app
from Halanweb.forms import RegistrationForm, LoginForm,UpdateAccountForm, orderForm
from Halanweb.models import User, Order
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.middleware.dispatcher import DispatcherMiddleware


@app.route("/")
@app.route("/home")
def home():
    page= request.args.get("page",1,type=int)
    orders= Order.query.order_by(Order.order_date.desc()).paginate(page=page, per_page=5 )
    return render_template('home.html', orders=orders )

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext= os.path.splitext(form_picture.filename)
    picture_fn= random_hex +f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file= picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Your account has been updated","success")
        return redirect(url_for('account'))
    elif request.method =="GET":
        form.username.data= current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file,form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
   
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/orders/new",methods=['GET', 'POST'])
@login_required
def new_order():
    form = orderForm()
    if request.method=="POST":  
        if form.validate_on_submit():
            Order1= Order( client_contact_no=form.client_contact_no.data,
                            order_id=form.order_id.data,
                            client_city=form.client_city.data,
                            client_address=form.client_address.data,
                            sme_name=form.sme_name.data,
                            order_status=form.order_status.data,
                            order_reason_of_failure=form.order_reason_of_failure.data,
                            driver_name=form.driver_name.data,
                            order_delivery_fees=form.order_delivery_fees.data,
                            order_value=form.order_value.data,
                            order_date=form.order_date.data ,
                            author=current_user
                    )
            db.session.add(Order1)
            db.session.commit()
            flash('order has been added','success')
            return redirect(url_for('new_order'))
        else:
            print(form.errors)
            flash('Order adding failed','danger')
            redirect(url_for('new_order'))
        return render_template('create_order.html',title="New order",form=form)
    else:
        return render_template('create_order.html', title='Data Entry', form=form,legend='New Order')

@app.route("/orders/<int:order_id>")
def order(order_id):
    order= Order.query.get_or_404(order_id)
    return render_template('order.html', order=order )


@app.route("/orders/<int:order_id>/update",methods=["GET","POST"])
@login_required
def update_order(order_id):
    order= Order.query.get_or_404(order_id)
    if order.author != current_user:
        abort(403)
    form= orderForm()

    if form.validate_on_submit():
        order.order_id=form.order_id.data
        order.order_status=form.order_status.data
        order.order_value=form.order_value.data
        flash('Your order has been updated!','sucess')
        return redirect(url_for('order',order_id=order.order_id))
    return render_template('create_order.html',
                           form=form, legend='Update order')


@app.route("/orders/<int:order_id>/delete",methods=["POST"])
@login_required
def delete_order(order_id):
    order= Order.query.get_or_404(order_id)
    if order.author != current_user:
        abort(403)
    db.session.delete(order)
    db.session.commit()
    flash('Your order has been Deleted!','danger')
    return redirect(url_for('home'))



@app.route("/user/<string:username>")
def user_orders(username):

    page= request.args.get("page",1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    orders= Order.query.filter_by(author=user)\
        .order_by(Order.order_date.desc())\
        .paginate(page=page, per_page=5 )
    return render_template('user_orders.html', orders=orders, user=user )

@app.route('/dashboard/')
def render_dashboard():
    return flask.redirect('/dashboard')


@app.route('/reports/')
def render_reports():
    return flask.redirect('/dash2')
