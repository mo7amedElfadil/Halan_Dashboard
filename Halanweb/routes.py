
from PIL import Image
import secrets
import os
import json
import plotly
from flask import render_template, url_for, flash, redirect, request,abort
from Halanweb import db, bcrypt, app
from Halanweb.forms import RegistrationForm, LoginForm,UpdateAccountForm, DeoOrderForm,AccountantUpdateOrderForm
from Halanweb.models import User, Order
from flask_login import login_user, current_user, logout_user, login_required
from dash_application.data import data
from dash_application.input_data import input_data, insert_data,update_data
from dash_application.upload_data import parseCSV
from dash_application.plots import report_plots
from dash_application.static_dicts import graph_description
from Halanweb.order_id_gen import order_id_generator
from Halanweb.main_graphs import *
from dash_application.regression import plot_prediction


sme_main = input_data()

@app.route("/", methods=['GET', 'POST'])
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
    return render_template('login2.html', title='Login', form=form)

@app.route("/home")
@login_required
def home():
    if current_user.role == "Upper Management":
        # data1 = data.halan_dataframes(sme_main,'order_status_count','Delivered','Monthly','SME')
        # data1 =  data1[data1['order_count']>100]
        # labs = data1['sme_name'].tolist()
        # dt = data1['order_count'].tolist()
        graphJSON1 =[]
        graph_title=[]
    
        
        graph = gmv_plot_monthly(sme_main)       
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        

        graph = gmv_plot_weekly(sme_main)
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
       
       
        
        graph = delivered_plot_monthly(sme_main)
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
       
    
        
        graph = delivered_plot_weekly(sme_main)
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
      

        graph = received_plot_monthly(sme_main)
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
       

        graph = received_plot_weekly(sme_main)
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
       

       
        
        length = len(graphJSON1)
        

        return render_template('home.html', graphJSON1 = graphJSON1 ,graph_title='Upper Management View',length=length) #labels=labs,values=dt,
    
    
    elif current_user.role == "admin":
      
       
        graphJSON1 =[]
       
       
        graph = guage_plot(data.summary_data(sme_main,'today_orders',),"Todays Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'week_orders',),"This week's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'month_orders',),"This month's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        
      
   
        # order list 
        page= request.args.get("page",1,type=int)
        orders= Order.query.order_by(Order.order_id.desc()).paginate(page=page, per_page=5 )
        length = len(graphJSON1)
        
        return render_template('home.html', orders=orders,graphJSON1 = graphJSON1 ,graph_title="Admin View",length=length) 

    elif current_user.role == "Data Entry Officer":
        page= request.args.get("page",1,type=int)
        orders= Order.query.order_by(Order.order_id.desc()).paginate(page=page, per_page=5 )
       
        graphJSON1 =[]
       
       
        graph = guage_plot(data.summary_data(sme_main,'today_orders',),"Todays Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'week_orders',),"This week's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'month_orders',),"This month's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        
      
        length = len(graphJSON1)
        return render_template('home.html', orders=orders,graphJSON1 = graphJSON1 , graph_title='Data Entry Officer View',length=length)
   
    elif current_user.role == "Drivers Supervisor":
        graphJSON1 =[]
       
       
        graph = guage_plot(data.summary_data(sme_main,'today_orders',),"Todays Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'week_orders',),"This week's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'month_orders',),"This month's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        
        #pending orders
        txt = data.summary_data(sme_main,'driver_summary')
        
        # order list 
        page= request.args.get("page",1,type=int)
        orders= Order.query.order_by(Order.order_id.desc()).paginate(page=page, per_page=5 )
        length = len(txt)
        
        return render_template('home.html', orders=orders,graphJSON1 = graphJSON1 ,length=length,graph_title="Drivers Supervisor View",txt=txt) #labels=labs,values=dt,

    elif current_user.role == "Accountant":
        graphJSON1 =[]
       
        graph = guage_plot(data.summary_data(sme_main,'today_orders',),"Todays Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'week_orders',),"This week's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'month_orders',),"This month's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        #pending orders
        txt = data.summary_data(sme_main,'driver_summary_acc')
   
        # order list 
        page= request.args.get("page",1,type=int)
        orders= Order.query.order_by(Order.order_id.desc()).paginate(page=page, per_page=5 )
        length = len(txt)
        
        return render_template('home.html', orders=orders,graphJSON1 = graphJSON1 ,length=length,graph_title="Accountant View",txt=txt) #labels=labs,values=dt,

    elif current_user.role == "Operations Manager":
        graphJSON1 =[]
       
        graph = guage_plot(data.summary_data(sme_main,'today_orders',),"Todays Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'week_orders',),"This week's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        graph = guage_plot(data.summary_data(sme_main,'month_orders',),"This month's Orders")
        graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
      
        
        #pending orders
        txt = data.summary_data(sme_main,'store_summary')
        
        # order list 
        page= request.args.get("page",1,type=int)
        orders= Order.query.order_by(Order.order_id.desc()).paginate(page=page, per_page=5 )
        length = len(txt)
        
        return render_template('home.html', orders=orders,graphJSON1 = graphJSON1 ,length=length,graph_title="Operations Manager View",txt=txt) #labels=labs,values=dt,

@app.route("/drivers")
def drivers():
    
    graphJSON1 =[]
    graph =report_plots.plots_treemap_main(sme_main,'Driver')
    
    graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
    graph  =report_plots.plots_traces(data.halan_dataframes(sme_main,'order_status_count','Delivered','Weekly','Driver'),'Driver','Weekly') 
    graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
    return render_template('drivers.html',graphJSON1 = graphJSON1 )

@app.route("/stores")
def stores():
    
    graphJSON1 =[]
    graph =report_plots.plots_treemap_main(sme_main,'SME')
    
    graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
    graph  =report_plots.plots_traces(data.halan_dataframes(sme_main,'order_status_count','Delivered','Weekly','SME'),'SME','Weekly')
    graphJSON1.append(json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder))
    return render_template('stores.html',graphJSON1 = graphJSON1 )

@app.route('/dash')
@login_required
def mini_dashboard():
    x=1
    return render_template('dashboard.html')

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
   
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/orders/new",methods=['GET', 'POST'])
@login_required
def new_order():
    form = DeoOrderForm()
    if request.method=="POST":  
        if form.validate_on_submit():
            Order1= Order( order_id=form.order_id.data, 
                            client_contact_no=form.client_contact_no.data,
                            client_city=form.client_city.data,
                            client_address=form.client_address.data,
                            sme_name=form.sme_name.data,
                            driver_name=form.driver_name.data,
                            order_delivery_fees=form.order_delivery_fees.data,
                            order_value=form.order_value.data,
                            order_status="Distributed",
                            order_reason_of_failure=form.order_reason_of_failure.data,
                            order_date=form.order_date.data ,
                            author=current_user
                    )
            records= (form.order_id.data,form.client_contact_no.data,form.client_city.data,
            form.client_address.data,form.sme_name.data,form.driver_name.data,
            form.order_delivery_fees.data,form.order_value.data,"Received",form.order_reason_of_failure.data,
            form.order_date.data )
            insert_data(records)

            db.session.add(Order1)
            db.session.commit()
            
            flash('order has been added','success')
            return redirect(url_for('new_order'))
        else:
            print(form.errors)
            flash('Order adding failed','danger')
            redirect(url_for('new_order'))
        return render_template('Deo_Update_Order.html',title="New order",form=form)
    else:
        return render_template('Deo_Update_Order.html', title='Data Entry', form=form,legend='New Order')



@app.route("/orders/csv",methods=['GET', 'POST'])
@login_required
def save_csv():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.root_path, 'static/csv', uploaded_file.filename)
          # set the file path
        uploaded_file.save(file_path)
          # save the file
        user_id = 1
        parseCSV(file_path,user_id)
    return redirect(url_for('new_order'))




@app.route("/orders/<int:order_id>")
@login_required
def order(order_id):
    order= Order.query.get_or_404(order_id)
    return render_template('order.html',title=order_id, order=order )


@app.route("/orders/<int:order_id>/update",methods=["GET","POST"])
@login_required
def update_order(order_id):
    order= Order.query.get_or_404(order_id)
          
    if current_user.role == "Data Entry Officer" :
        form= DeoOrderForm()
        if form.validate_on_submit():
            order.client_contact_no=form.client_contact_no.data
            order.client_city=form.client_city.data
            order.client_address=form.client_address.data
            order.sme_name=form.sme_name.data
            order.order_status=form.order_status.data
            order.order_reason_of_failure=form.order_reason_of_failure.data
            order.driver_name=form.driver_name.data
            order.order_delivery_fees=form.order_delivery_fees.data
            order.order_value=form.order_value.data
            order.order_date=form.order_date.data   
           
            records= ( form.driver_name.data, form.order_delivery_fees.data,form.order_value.data,"Received",form.order_reason_of_failure.data,
            form.order_date.data ,form.order_id.data)
            update_data(records)

            db.session.commit()
            flash('Your order has been updated!','sucess')
            return redirect(url_for('home'))

        elif request.method =="GET":
            form.order_id.data= order.order_id
            form.order_status.data=order.order_status
            form.client_contact_no.data=order.client_contact_no
            form.order_value.data= order.order_value
            form.client_city.data=order.client_city
            form.client_address.data=order.client_address
            form.sme_name.data=order.sme_name
            form.order_status.data=order.order_status
            form.order_reason_of_failure.data=order.order_reason_of_failure
            form.driver_name.data=order.driver_name
            form.order_delivery_fees.data=order.order_delivery_fees
            form.order_value.data=order.order_value
            form.order_date.data=order.order_date
            return render_template('Deo_Update_Order.html',
                                                    form=form, legend='Update Order {}'.format(form.order_id.data))
    elif current_user.role == "Accountant" :
        form= AccountantUpdateOrderForm()
        if form.validate_on_submit():
            order.client_contact_no=form.client_contact_no.data
            order.client_city=form.client_city.data
            order.client_address=form.client_address.data
            order.sme_name=form.sme_name.data
            order.order_status=form.order_status.data
            order.order_reason_of_failure=form.order_reason_of_failure.data
            order.driver_name=form.driver_name.data
            order.order_delivery_fees=form.order_delivery_fees.data
            order.order_value=form.order_value.data
            order.order_date=form.order_date.data       
            db.session.commit()
            flash('Your order has been updated!','sucess')
            return redirect(url_for('home'))

        elif request.method =="GET":
            form.order_id.data= order.order_id
            form.order_status.data=order.order_status
            form.client_contact_no.data=order.client_contact_no
            form.order_value.data= order.order_value
            form.client_city.data=order.client_city
            form.client_address.data=order.client_address
            form.sme_name.data=order.sme_name
            form.order_status.data=order.order_status
            form.order_reason_of_failure.data=order.order_reason_of_failure
            form.driver_name.data=order.driver_name
            form.order_delivery_fees.data=order.order_delivery_fees
            form.order_value.data=order.order_value
            form.order_date.data=order.order_date
        return render_template('Accountant_Update_Order.html',
                                            form=form, legend='Update Order {}'.format(form.order_id.data))
    elif current_user.role  != ["Data Entry Officer","Accountant"]:
        abort(403)
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
@login_required
def user_orders(username):

    page= request.args.get("page",1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    orders= Order.query.filter_by(author=user)\
        .order_by(Order.order_id.desc())\
        .paginate(page=page, per_page=5 )
    return render_template('user_orders.html', orders=orders, user=user )


