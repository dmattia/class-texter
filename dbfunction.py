import sqlite3 as lite

# Adds a form submission to the database
def add_row(form):
	""" Get data from form
	

	"""	
	crn = form['crn']
	number = "+1" + form['phone_number']
	verified = 0

	# Connect to db
	data = [crn, number, verified]
	conn = lite.connect('/home/flask/class_text/submissions.db')
	
	# Add row to db
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO user_submission VALUES(?,?,?)',(data,))

	return True

# Update a phone number after an 'accept' reply
def verify_number(number):
	conn = lite.connect('/home/flask/class_text/submissions.db')
	with conn:
		c = conn.cursor()
		c.execute("UPDATE user_submission SET verified = 1 WHERE number = '%s'" % number)
