from flask import Blueprint,render_template, request, redirect, url_for, session,flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bcrypt #pip install bcrypt https://pypi.org/project/bcrypt/
from database import mysql
from flask_mysqldb import MySQLdb

customer = Blueprint('customer', __name__, url_prefix='/', template_folder='templates',static_folder="static")


@customer.route('/')
@customer.route('/index')
def customer_index():
    return render_template('customer/index.html')

@customer.route('/profile')
def profile():
    return render_template('customer/profile.html')

@customer.route('/register', methods=["GET", "POST"]) 
def register():
    try:
        if request.method == 'GET':
            return render_template("customer/register.html")
        elif request.method == 'POST':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT email FROM users")
            user = curl.fetchall()
            curl.close()
            if request.form['email'] == user:
                flash('Mail already exist')  
                return redirect(url_for('customer.register'))
            else:
                name = request.form['name']
                email = request.form['email']
                password = request.form['password'].encode('utf-8')
                hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
                mysql.connection.commit()
                session['name'] = request.form['name']
                session['email'] = request.form['email']
                return redirect(url_for('customer.customer_index'))
    except:
        flash('Mail already exist')  
        return redirect(url_for('customer.register'))


@customer.route('/login',methods=["GET","POST"])
def cu_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                # return('1')
                return render_template("customer/index.html")
            else:
                flash('Error password and email not match')
                return redirect(url_for('customer.cu_login'))
                # return render_template("customer/error.html")
                # return "Error password and email not match"
        else:
            flash('user not found! please register.')
            return redirect(url_for('customer.cu_login'))
            # return render_template("customer/notfound.html")
            # return("Error user not found")
    else:
        return render_template("customer/index.html")

 
@customer.route('/logout')
def logout():
    session.clear()
    return render_template("customer/index.html")


@customer.route('/reset_request')
def reset_request():
    return render_template("customer/reset_request.html")


