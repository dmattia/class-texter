from flask import Flask, render_template, request, url_for, redirect
from dbfunction import add_row
from Get_Sorted_CRNs import is_Valid, Get_Crns

sorted_crn_numbers, crn_dict = Get_Crns()


app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def hello_world():
	if request.method == 'POST':
		if not is_Valid(request.form["crn"], sorted_crn_numbers):
			print "Invalid CRN" 
			return render_template('home.html')
			pass
		else:
			add_row(request.form)
			url = url_for("thank_you", Num = request.form['phone_number'])
			return redirect(url)
	else:
		return render_template('home.html')

@app.route('/thanks/<Num>')
def thank_you(Num):
	number = format_phone_number(Num)
	return render_template('thanks.html', number=number)

def format_phone_number(number):
	str_num = str(number)
	return str_num[:2] + '(' + str_num[2:5] + ')' + str_num[5:8] + '-' + str_num[8:]

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
