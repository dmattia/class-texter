from twilio.rest import TwilioRestClient
import os



ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

messages = client.messages.list()

for message in messages:
	if message.to == TWILIO_NUMBER:  
		if message.body.lower() == "yes" or message.body.lower() == "yes " :
	 		message = client.messages.create(to= message.from_, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been verified! We will send you a message if a spot opens up in your course")
		elif message.body.lower() == "stop" or message.body.lower == "stop ":
			message = client.messages.create(to= message.from_, from_=TWILIO_NUMBER, body="Thank you for the reply, your number has been disconnected. You will no longer receive messages unless you resign up!")
		else:
			message = client.messages.create(to= message.from_, from_=TWILIO_NUMBER, body="We cannot understand your response. Please reponse 'yes' if you'd like to receive a text alert if a spot opens in your selected course and 'stop' if you'd like to no longer receive messages")

