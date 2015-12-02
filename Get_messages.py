from twilio.rest import TwilioRestClient
from dbfunction import verify_number
from time import sleep
import os

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





