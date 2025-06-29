'''
import all flask extensions (the lazy way)
import sqlite3
'''
from flask import *
import sqlite3 as db
'''
import from second file
'''
from admin.admin import admin
'''
deploy using waitress WSGI
'''
# from waitress import serve # Removed for Gunicorn

app = Flask(__name__)
app.secret_key = 'nooneshouldknow'
'''
registering the blueprint from the second file (app.py)
'''
app.register_blueprint(admin, url_prefix = "/admin")
'''
select data
'''
@app.route('/select/<string:id>')
def select(id):
	conn = db.connect('RDBMS.db')
	cur = conn.cursor()

	stmt = """
		SELECT * FROM student_data WHERE stud_id = ?
	"""
	cur.execute(stmt, (id,))

	rw = cur.fetchall()
	return render_template('select.html', rows = rw)
'''
for searching records
'''
@app.route('/search', methods = ['GET', 'POST'])
def usersearch():
	if request.method == 'POST':
		conn = db.connect('RDBMS.db')
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
		return render_template('records.html', row = result)
	else:
		return render_template('records.html', row = result)
'''
for running the front page (landing page)
'''
@app.route('/')
def index():
	return render_template('landingpage.html')

dev_mode = True

if __name__ == '__main__':
	if dev_mode == True:
		app.run(port = 5555, debug = True)
	else:
		# Gunicorn will be used to serve the app in production.
		# Example command: gunicorn -w 4 -b 0.0.0.0:5555 app:app
		# This script will typically not reach the 'else' block when run by Gunicorn,
		# as Gunicorn imports the 'app' object directly.
		# If run directly in a non-dev production setup (not recommended),
		# it would simply do nothing here, relying on an external Gunicorn process.
		pass
