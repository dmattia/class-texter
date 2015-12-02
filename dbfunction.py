import sqlite3 as lite
from Get_Sorted_CRNs import Write_Courses
from Get_messages import Send_Text

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

def Check_for_openings():

	courses = Write_Courses()
	# for course in courses:
	# 	if course["CRN"] == ""
	conn = lite.connect('/home/flask/class_text/submissions.db')
	with conn:
		c = conn.cursor()
		query = "Select * From user_submission Where verified = 1"
		c.execute(query)
		a = c.fetchall()
		for query in a:
			for course in courses:
				if str(query[0]) == course["CRN"]:
					if int(course["Opn"]) > 0:
						Send_Text(str(query[1]), course)
						new_query = "Delete from user_submission where crn = " + str(query[0]) + " and number = '" + str(query[1]) + "' and verified = " + str(query[2])
						c.execute(new_query)
					else:
		


Check_for_openings()
# Update a phone number after an 'accept' reply
def verify_number(number):
	conn = lite.connect('/home/flask/class_text/submissions.db')
	with conn:
		c = conn.cursor()
		c.execute("UPDATE user_submission SET verified = 1 WHERE number = '%s'" % number)

