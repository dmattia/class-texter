from twilio.rest import TwilioRestClient
from dbfunction import verify_number
from Get_Sorted_CRNs import Get_Courses
from time import sleep
import sqlite3 as lite
import os


def Check_for_openings():
 	conn = lite.connect('/home/flask/class_text/submissions.db')

 	with conn:
 		c = conn.cursor()
 		query = "Select * From user_submission Where verified = 1"
 		c.execute(query)
 		a = c.fetchall() 
 		if i is not None:
 			for query in a:
 				courses = Get_Courses(str(query[3]))
 				for course in courses:
 					if str(query[0]) == course["CRN"]:
 						if int(course["Opn"]) > 0:
 							Send_Text(str(query[1]), course)
 							new_query = "Delete from user_submission where crn = " + str(query[0]) + " and number = '" + str(query[1]) + "' and verified = " + str(query[2]) + " and  Department = '" + str(query[3]) + "'"
 							c.execute(new_query)

# def Check_for_openings():
# 	conn = lite.connect('/home/flask/class_text/submissions.db')
	
# 	courses_iter = Write_Courses_iter()
# 	for i in courses_iter:
# 		courses = i
# 		with conn:
# 			c = conn.cursor()
# 			query = "Select * From user_submission Where verified = 1"
# 			c.execute(query)
# 			a = c.fetchall()
# 			if a is not None:
# 				for query in a:
# 					for course in courses:
# 						if str(query[0]) == course["CRN"]:
# 							if int(course["Opn"]) > 0:
# 								Send_Text(str(query[1]), course)
# 								new_query = "Delete from user_submission where crn = " + str(query[0]) + " and number = '" + str(query[1]) + "' and verified = " + str(query[2])
# 								c.execute(new_query)
	
def Send_Reply_verification(phone_number = None):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	
	#messages = client.messages.list(from_ = phone_number).reverse() # Reversed to respond to the earliest messages first
	messages = client.messages.list(from_ = phone_number)

	did_receive = False
	if messages is not None:
		for message in messages:
			body = message.body.lower().strip()
			if body == "accept":
				verify_number(phone_number)
			 	client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been verified! We will send you a message if a spot opens up in your course")
			elif body == "deny":
				remove_number(phone_number)
				client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been disconnected. You will no longer receive messages unless you resign up!")
				message_text = message.body.lower()
				did_receive = True
				#client.messages.delete(message.sid)
			else:
				client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="We cannot understand your response. Please reply 'yes' if you'd like to receive a text alert if a spot opens in your selected course, or 'stop' if you'd like to no longer receive messages")
			
			message_text = message.body.lower()
			did_receive = True
			client.messages.delete(message.sid)
	if did_receive:
		return message_text
	else:
		return "No message received"


def Send_Reply_Inquiry(phone_number = None):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	try:
		client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for signing up! To verify, Please reply 'accept' if you'd like to receive a text alert if a spot opens in your selected course, or 'deny' if you'd like to no longer receive messages")
		return "Success"
	except:
		return "Invalid phone Number"

def Send_Text(phone_number, course):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')


	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	try:
		client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Attenion!!!! " + course["Title"] + " ( "+ course["Course - Sec"] + " ) at " + course["When"] + " now has " + course["Opn"] + " openings! CRN = " + course["CRN"])
	except:
		print "Invalid phone Number"

def Check_For_Responses():
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '') 

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	messages = client.messages.list()
	for message in messages:
		if message.from_ != TWILIO_NUMBER:
			Send_Reply_verification(message.from_)
			#client.messages.delete(message.sid)





