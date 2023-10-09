from flask import Response, Flask, render_template, request, make_response, session, redirect, url_for, escape, abort, flash, g, jsonify
import sqlite3 as sql
import os
import flask_sijax
from flask_sqlalchemy import SQLAlchemy
# from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "any random string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

db = SQLAlchemy(app)
class students(db.Model):
	id = db.Column('student_id', db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	city = db.Column(db.String(50))  
	addr = db.Column(db.String(200))
	pin = db.Column(db.String(10))

	def __init__(self, name, city, addr,pin):
		self.name = name
		self.city = city
		self.addr = addr
		self.pin = pin

@app.route('/hello/<int:score>')
def hello_name(score):
	return render_template('example.html', marks = score)

@app.route('/check_result')
def check_result():
	dict = {'phy':50,'che':60,'maths':70}
	return render_template('example.html', result = dict)

@app.route('/', methods = ['GET'])
def index():
	# if 'username' in session:
	# 	username = session['username']
	# 	return 'Logged in as ' + username + '<br>' + \
	# 	"<b><a href = '/logout'>click here to log out</a></b>" + \
	# 		render_template('student.html')
	# return "You are not logged in <br><a href = '/login'></b>" + \
	# 	"click here to log in</b></a>" + render_template('student.html')
	con = sql.connect("database.db")
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("select * from students")

	rows = cur.fetchall()
	return render_template('student.html', students = students.query.all(), rows = rows)

@app.route('/', methods = ['POST'])
def new():
	if request.method == 'POST':
		if not request.form['name'] or not request.form['city'] or not request.form['addr']:
			flash('Please enter all the fields', 'error')
		else:
			student = students(request.form['name'], request.form['city'],
			request.form['addr'], request.form['pin'])
			
			db.session.add(student)
			db.session.commit()
			
			flash('Record was successfully added')
			return redirect(url_for('index'))
	return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result = result)

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
	if request.method == 'POST':
		user = request.form['nm']

	resp = make_response(render_template('readcookie.html'))
	resp.set_cookie('userID', user)

	return resp

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome '+name+'</h1>'

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != 'admin' or \
			request.form['password'] != 'admin':
			error = 'Invalid username or password. Please try again!'
			return render_template('student.html', error = error)
			# abort(401)
		else:
			session['username'] = request.form['username']
			flash('You were successfully logged in')
			# return redirect(url_for('success'))
			return redirect(url_for('index'))
	else:
		return '''
		
		<form action = "" method = "post">
			<p><input type = text name = "username"></p>
			<p><input type = submit value = Login></p>
		</form>
		<a href = '/'>back to home</a>
		'''

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	# if request.method == 'POST':
	# 	f = request.files['file']
	# 	f.save(secure_filename(f.filename))
	# 	return 'file uploaded successfully'
	return redirect(url_for('index'))

@app.route('/success')
def success():
	return 'logged in successfully' + '<br>' \
		"<b><a href = '/logout'>click here to log out</a></b>"

@app.route('/logout')
def logout():
	# remove the username from the session if it is there
	session.pop('username', None)
	return redirect(url_for('index'))
	# redirect(location, statuscode, response)

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		try:
			nm = request.form['nm']
			addr = request.form['add']
			city = request.form['city']
			pin = request.form['pin']
			
			with sql.connect("database.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
			
			con.commit()
			msg = "Record successfully added"
		except:
			con.rollback()
			msg = "error in insert operation"
		finally:
			return render_template("result.html", msg = msg)
			con.close()

@flask_sijax.route(app, '/hello')
def hello():
	def say_hi(obj_response):
		obj_response.alert('Hi there!')
	if g.sijax.is_sijax_request:
		# Sijax request detected - let Sijax handle it
		g.sijax.register_callback('say_hi', say_hi)
		return g.sijax.process_request()
	return render_template('student.html')

if __name__ == '__main__':

	conn = sql.connect('database.db')
	print("Opened database successfully")

	# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
	print("Table created successfully")
	conn.close()

	db.create_all()
    
	app.run(host="127.0.0.1", port="8000", debug=True,
		threaded=True, use_reloader=False)