from flask import Flask, render_template, request, url_for, redirect, g
from Get_messages  import Send_Reply_Inquiry
from Get_Sorted_CRNs import is_Valid, Get_CRN_List
from dbfunction import add_row
import sqlite3
import os

DATABASE = '/home/flask/class_text/submissions.db'
SECRET_KEY = os.environ.get('TEXTING_SECRET_KEY','')

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['GET','POST'])
def hello_world():
	if request.method == 'POST':
		sorted_crn_numbers = Get_CRN_List()
		#if not is_Valid(request.form["crn"], sorted_crn_numbers):
		if False:
			print "Invalid CRN" 
			return render_template('home.html')
		else:
			add_row(request.form)
			Message = Send_Reply_Inquiry('+1' + request.form["phone_number"])
			url = url_for("thank_you", Num = request.form['phone_number'])
			return redirect(url)
	else:
		return render_template('home.html')

@app.route('/thanks/<Num>')
def thank_you(Num):
	number = format_phone_number("+1" + Num)
	return render_template('thanks.html', number=number)

@app.route('/message/')
def message(message):
	return render_template('message.html', message=message)

def format_phone_number(number):
	str_num = str(number)
	return str_num[:2] + '(' + str_num[2:5] + ')' + str_num[5:8] + '-' + str_num[8:]

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
