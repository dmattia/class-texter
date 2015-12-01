import sqlite3 as lite

# Adds a form submission to the database
def add_row(form):
	# Get data from form
	crn = form['crn']
	number = "+1" + form['phone_number']
	verified = 0

	# Connect to db
	data = [crn, number, verified]
	conn = lite.connect('submissions.db')
	c = conn.cursor()

	# Add row to db
	c.executemany('INSERT INTO user_submission VALUES(?,?,?)',(data,))
