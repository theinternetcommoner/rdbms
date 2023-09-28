from flask import *
from functools import wraps
import sqlite3 as db
# from waitress import serve

admin = Blueprint("admin", __name__, static_folder = "static", template_folder = "templates")

def login_required(f):
	@wraps(f)
	def _login_required(*args, **kwargs):
		if session.get('usr'):
			return f(*args, **kwargs)
		else:
			return redirect(url_for('admin.loginPage'))
	return _login_required
'''
update data
'''
@admin.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
	if request.method == 'POST':
		try:
			idval = request.form['id']
			firstname = request.form['fname']
			middlename = request.form['mname']
			lastname = request.form['lname']
			schoolname = request.form['schname']
			schooladdress = request.form['schaddress']

			with db.connect('./RDBMS.db') as conn:
				cur = conn.cursor()

				sqlStudent = """
					UPDATE tbl_student SET f_name = ?, m_name = ?, l_name = ?
					WHERE stud_id = ?
				"""
				cur.execute(sqlStudent, (firstname, middlename, lastname, idval))

				sqlSchool = """
					UPDATE tbl_school SET sch_name = ?, sch_address = ?
					WHERE sch_id = ?
				"""
				cur.execute(sqlSchool, (schoolname, schooladdress, idval))
							
				conn.commit()
				msg = 'success!'
		except:
			conn.rollback()
			msg = 'failed!'
		finally:
			return render_template('result.html', message = msg)
			conn.close()

'''
select data to update
'''
@admin.route('/selectupdate/<string:id>')
@login_required
def selectup(id):
	conn = db.connect('./RDBMS.db')
	cur = conn.cursor()

	stmt = """
		SELECT * FROM student_data WHERE stud_id = ?
	"""
	cur.execute(stmt, (id,))

	rw = cur.fetchall()
	#for testing purposes
	# for x in rw:
	# 	# return x[0]+x[1]
	return render_template('selectup.html', rows = rw)

'''
list of data plus update link
'''
@admin.route('/listupdate')
@login_required
def listup():
	conn = db.connect('./RDBMS.db')
	conn.row_factory = db.Row

	query = conn.cursor()
	sql = """
		SELECT * FROM student_data
	"""
	query.execute(sql)

	result = query.fetchall()
	return render_template('listup.html', row = result)

'''
delete data from database
'''
@admin.route('/deletedata/<string:id>')
@login_required
def deleterecord(id):
	try:
		with db.connect('./RDBMS.db') as conn:
			cur = conn.cursor()

			query1 = """
				DELETE FROM tbl_student WHERE stud_id = ?
			"""
			cur.execute(query1, (id,))

			query2 = """
				DELETE FROM tbl_school WHERE sch_id = ?
			"""
			cur.execute(query2, (id,))

			query3 = """
				DELETE FROM tbl_conn WHERE id = ?
			"""
			cur.execute(query3, (id,))

			conn.commit()
			msg = 'success!'
	except:
		conn.rollback()
		msg = 'failed!'
	finally:
		return render_template('result.html', message = msg)
		conn.close()

'''
select data to delete
'''
@admin.route('/selectdelete/<string:id>')
@login_required
def selectdel(id):
	conn = db.connect('./RDBMS.db')
	cur = conn.cursor()

	stmt = """
		SELECT * FROM student_data WHERE stud_id = ?
	"""
	cur.execute(stmt, (id,))

	rw = cur.fetchall()
	#for testing purposes
	# for x in rw:
	# 	# return x[0]+x[1]
	return render_template('selectdel.html', rows = rw)

'''
list of data plus delete link
'''
@admin.route('/listdelete')
@login_required
def listdel():
	conn = db.connect('./RDBMS.db')
	conn.row_factory = db.Row

	query = conn.cursor()
	sql = """
		SELECT * FROM student_data
	"""
	query.execute(sql)

	result = query.fetchall()
	return render_template('listdel.html', row = result)

'''
insert form
'''
@admin.route('/new')
@login_required
def newform():
	return render_template('newform.html')

'''
adding new record
'''
@admin.route('/insert', methods = ['GET', 'POST'])
@login_required
def insertrecord():
	if request.method == 'POST':
		try:
			firstname = request.form['fname']
			middlename = request.form['mname']
			lastname = request.form['lname']
			schoolname = request.form['schname']
			schooladdress = request.form['schaddress']

			with db.connect('./RDBMS.db') as conn:
				cur = conn.cursor()

				sqlStudent = """
					INSERT INTO tbl_student(f_name, m_name, l_name)
					VALUES(?, ?, ?)
				"""
				cur.execute(sqlStudent, (firstname, middlename, lastname))

				sqlSchool = """
					INSERT INTO tbl_school(sch_name, sch_address)
					VALUES(?, ?)
				"""
				cur.execute(sqlSchool, (schoolname, schooladdress))

				sqlstudid = """
					SELECT * FROM tbl_student ORDER BY stud_id DESC LIMIT 1
				"""
				cur.execute(sqlstudid)
				row1 = cur.fetchall()
				for s1 in row1:
					s1[0]

				sqlschid = """
					SELECT * FROM tbl_school ORDER BY sch_id DESC LIMIT 1
				"""
				cur.execute(sqlschid)
				row2 = cur.fetchall()
				for s2 in row2:
					s2[0]

				studentid = s1[0]
				schoolid = s2[0]
							
				sqlconn = """
					INSERT INTO tbl_conn(stud_id, sch_id)
					VALUES(?, ?)
				"""
				cur.execute(sqlconn, (studentid, schoolid))
							
				conn.commit()
				msg = 'success!'
		except:
			conn.rollback()
			msg = 'failed!'
		finally:
			return render_template('result.html', message = msg)
			conn.close()
'''
for searching records
'''
@admin.route('/search', methods = ['GET', 'POST'])
@login_required
def searchrecord():
	if request.method == 'POST':
		conn = db.connect('./RDBMS.db')
		conn.row_factory = db.Row

		query = conn.cursor()
		searchVal = request.form['search']
		sql = """
			SELECT * FROM student_data WHERE
			stud_id LIKE ? OR
			f_name LIKE ? OR
			m_name LIKE ? OR
			l_name LIKE ? OR
			sch_name LIKE ? OR
			sch_address LIKE ?
		"""
		query_inputs = ('%'+searchVal+'%', '%'+searchVal+'%', '%'+searchVal+'%', '%'+searchVal+'%', '%'+searchVal+'%', '%'+searchVal+'%')
		query.execute(sql, query_inputs)

		result = query.fetchall()
		return render_template('list.html', row = result)
	else:
		return render_template('list.html', row = result)
'''
for viewing all records
'''
@admin.route('/view')
@login_required
def viewrecord():
	conn = db.connect('./RDBMS.db')
	conn.row_factory = db.Row

	query = conn.cursor()
	sql = """
		SELECT * FROM student_data
	"""
	query.execute(sql)

	result = query.fetchall()
	return render_template('list.html', row = result)

'''
for running the front page (landing page)
'''
@admin.route('/')
def index():
	if 'usr' in session:
		return render_template('index.html')
	return redirect(url_for('admin.loginPage'))
'''
login authentication
'''
@admin.route('/login')
def loginPage():
	return render_template('login.html')

@admin.route('/logincheck', methods = ['GET', 'POST'])
def logincheck():
	if request.method == 'POST':
		try:
			conn = db.connect('./RDBMS.db')
			cur = conn.cursor()

			stmt = """
				SELECT * FROM tbl_accounts WHERE username = ?
			"""
			cur.execute(stmt, (request.form['usr'],))

			rw = cur.fetchall()
			for x in rw:
				x
			session['usr'] = x[1]
			return redirect(url_for('admin.index'))
		except:
			return redirect(url_for('admin.loginPage'))

# @admin.route('/')
# def index():
# 	if 'usr' in session:
# 		#assign 'user' to session
# 		user = session['usr']
# 		return render_template('adminhome.html', user = user)
# 	return redirect(url_for('admin.loginPage'))

@admin.route('/logout')
def logout():
	#remove 'user' from session
	session.pop('usr', None)
	return redirect(url_for('index'))