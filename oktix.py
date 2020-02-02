#!/usr/bin/env python3
import requests, sys, time, urllib.parse, signal
from bs4 import BeautifulSoup

cookie = {
	'remember_user_token' : '',
	'kktix_session_token_v2': ''
}

def getCSRFToken(event):
	r = requests.get('https://kktix.com/events/{}/registrations/new'.format(event), cookies = cookie)
	soup = BeautifulSoup(r.text, 'html.parser')
	csrfTag = soup.find('meta', attrs = {'name':"csrf-token"})
	try:
		return csrfTag['content']
	except Exception as e:
		print('getCSRFToken Failed: {}\n{}'.format(repr(e), r.text))
		sys.exit(-1)

def getOrderToken(event, csrfToken, ticketId, ticketQuantity):
	csrfToken = urllib.parse.quote(csrfToken)
	orderInfo = """
		{"tickets":[{"id":%s,"quantity":%s,"invitationCodes":[],"member_code":"","use_qualification_id":null}],"currency":"TWD","recaptcha":{},"agreeTerm":true}
	""" % (ticketId, ticketQuantity)
	r = requests.post('https://queue.kktix.com/queue/{}?authenticity_token={}'.format(event, csrfToken), cookies = cookie, data = orderInfo)
	try:
		return r.json()['token']
	except:
		print(r.text)
		#print('getOrderToken Failed: {}\n{}'.format(repr(e), r.text))
		return -1

def getOrderId(orderToken):
	r = requests.get('https://queue.kktix.com/queue/token/{}'.format(orderToken), cookies = cookie)
	try:
		return r.json()['to_param']
	except Exception as e:
		print('getOrderId Failed: {}\n{}'.format(repr(e), r.text))
		sys.exit(-1)

def signal_handler(signal, frame):
	sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def main():
	if len(sys.argv) < 5:
		print('Usage: python3 oktix.py [Event] [Ticket ID] [Ticket Quantity] [Sleep Seconds]')
		sys.exit(-1)

	event = sys.argv[1]
	ticketId = sys.argv[2]
	ticketQuantity = sys.argv[3]
	sleepTime = float(sys.argv[4])

	csrfToken = getCSRFToken(event)
	while True:
		orderToken = getOrderToken(event, csrfToken, ticketId, ticketQuantity)
		time.sleep(sleepTime)
		if not orderToken is -1:
			break
	orderId = getOrderId(orderToken)

	print('https://kktix.com/events/{}/registrations/{}'.format(event, orderId))

if __name__ == '__main__':
	main()
