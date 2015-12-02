from twilio.rest import TwilioRestClient
import os

def Send_Reply_verification(phone_number = None):
	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	
	messages = client.messages.list(from_ = phone_number)

	did_receive = False
	for message in messages:
		if message.body.lower() == "accept" or message.body.lower() == "accept " or message.body.lower() == " accept":
			verify_number(phone_number)
		 	client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been verified! We will send you a message if a spot opens up in your course")
		elif message.body.lower() == "deny" or message.body.lower == "deny " or message.body.lower() == " deny":
			client.messages.create(to= phone_number, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been disconnected. You will no longer receive messages unless you resign up!")
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
			message = Send_Reply_verification(message.from_)
			print message


#Check_For_Responses()



