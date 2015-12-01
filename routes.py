from flask import Flask, render_template, request
import sqlite3 as lite

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello_world():
	if request.method == 'POST':
		crn = request.form['crn']
		number = "+1" + request.form['phone_number']
		verified = 0 # Defaults to false
		data = [crn, number, verified]

		conn = lite.connect('submissions.db')
		c = conn.cursor()
		c.executemany('INSERT INTO user_submission VALUES(?,?,?)',(data,))

		return thank_you(number)
	else:
		return render_template('home.html')

@app.route('/thanks/')
def thank_you(number):
	number = format_phone_number(number)
	return render_template('thanks.html', number=number)

def format_phone_number(number):
	str_num = str(number)
	return str_num[:2] + '(' + str_num[2:5] + ')' + str_num[5:8] + '-' + str_num[8:]

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
