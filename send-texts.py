from class_search_web_scrapping import GetClasses, GetCurrentSemester
from twilio.rest.exceptions import TwilioRestException
from twilio.rest import TwilioRestClient
import os



crn = '24680'
openSpots = 0
courseName = 'Unamed Course'
classes = GetClasses(GetCurrentSemester(), "CSE", "A", "0ANY", "A", "M")
for course in classes:
	if course['CRN'] == crn:
		openSpots = course['Opn']
		courseName = course['Title']

if int(openSpots) > 0:
	body = "A spot has recently opened up in a class you are watching on ndreviews.com\n\
The course %s now has %s open spots\n\
\n\
Good luck NOVOing as quick as you can!\n\
-ndreviews staff" % (courseName, openSpots)

	ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
	AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
	TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', '')

	try:
		client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
		message = client.messages.create(to="+16124378532", from_=TWILIO_NUMBER, body=body)
	except TwilioRestException:
		print "Invalid twilio settings. Set your environment variables in the ~/.bashrc file"
		exit(1)
	
	print "text sent"
else:
	print "text not sent"
