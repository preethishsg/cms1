from flask import Blueprint,render_template, request, redirect, url_for, session,flash
import bcrypt #pip install bcrypt https://pypi.org/project/bcrypt/
from database import mysql
from flask_mysqldb import MySQLdb

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates',static_folder='static')

@admin.route('/')
def admin_index():
    return render_template('admin/index.html')

@admin.route('/branchdb')
def branchdb():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM branchDb')
    data = cur.fetchall()
    cur.close()
    return render_template('admin/branchdb.html',contacts = data)

@admin.route('/admin/admin_login',methods=["GET","POST"])
@admin.route('/admin_login',methods=["GET","POST"])
def admin_login():   
    admin_email = 'admin123@gmail.com'
    admin_password = 'admin'
    admin_name = 'admin' 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
    #     curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     curl.execute("SELECT * FROM admindb WHERE email=%s",(email,))
    #     user = curl.fetchone()
    #     curl.close()
 
        if email == admin_email and password == admin_password:
            session['name'] = admin_name
            session['email'] = admin_email
            # return('1')
            return render_template("admin/index.html")
        else:
            flash('email and password not match')
            return redirect(url_for('admin.admin_login'))
    else:
        return render_template("admin/admin_login.html")

@admin.route('admin/decline/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM branchDb WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('admin.branchdb'))

@admin.route('admin/details/<string:id>')
def details(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM branchDb WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('admin/details.html',contacts = data)

@admin.route('/admin/ad_logout')
def ad_logout():
    session.clear()
    # return redirect(url_for('admin.admin_login'))
    return render_template("admin/admin_login.html")

