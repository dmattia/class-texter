from flask import Flask, render_template, request
from dbfunction import add_row
import os

app = Flask(__name__)
app.secret_key = os.environ.get('TEXTING_SECRET_KEY','')

@app.route('/', methods=['GET','POST'])
def hello_world():
	if request.method == 'POST':
		add_row(request.form)
		return thank_you("+1" + request.form['phone_number'])
	else:
		return render_template('home.html')

@app.route('/thanks/')
def thank_you(number):
	number = format_phone_number(number)
	return render_template('thanks.html', number=number)

@app.route('/message/')
def message(message):
	return render_template('message.html', message=message)

def format_phone_number(number):
	str_num = str(number)
	return str_num[:2] + '(' + str_num[2:5] + ')' + str_num[5:8] + '-' + str_num[8:]

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
