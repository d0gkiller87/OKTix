#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.parse
import requests
import signal
import json
import time
import sys

cookies = {
    'kktix_session_token_v2': ''
}

def getCSRFToken( event ):
    url = f"https://kktix.com/events/{ event }/registrations/new"
    print( f"-> { url }" )
    r = requests.get( url, cookies = cookies )
    soup = BeautifulSoup( r.text, 'html.parser' )
    csrfTag = soup.find( 'meta', attrs = { 'name' : 'csrf-token' } )
    try:
        return csrfTag['content']
    except Exception as e:
        raise RuntimeError( f"getCSRFToken Failed: { e }\n{ r.text }" )

def getOrderToken( event, csrfToken, ticketId, ticketQuantity ):
    csrfToken = urllib.parse.quote( csrfToken )
    orderInfo = json.dumps({
        "tickets": [{
            "id": int( ticketId ),
            "quantity": int( ticketQuantity ),
            "invitationCodes": [],
            "member_code": "",
            "use_qualification_id": None
        }],
        "currency": "TWD",
        "recaptcha": {},
        "agreeTerm": True
    })
    url = f"https://queue.kktix.com/queue/{ event }?authenticity_token={ csrfToken }"
    print( f"-> { url }" )
    r = requests.post( url, cookies = cookies, data = orderInfo )
    try:
        return r.json().get( 'token' )
    except Exception as e:
        raise RuntimeError( f"getOrderToken Failed: { e }\n{ r.text }" )

def getOrderId( orderToken ):
    url = f"https://queue.kktix.com/queue/token/{ orderToken }"
    print( f"-> { url }" )
    r = requests.get( url, cookies = cookies )
    try:
        return r.json()['to_param']
    except Exception as e:
        raise RuntimeError( f"getOrderId Failed: { e }\n{ r.text }" )

def signal_handler( signal, frame ):
    sys.exit()
signal.signal( signal.SIGINT, signal_handler )

def main():
    if len( sys.argv ) < 5:
        print( 'Usage: python3 oktix.py [Event] [Ticket ID] [Ticket Quantity] [Sleep Seconds]' )
        return

    event = sys.argv[1]
    ticketId = sys.argv[2]
    ticketQuantity = sys.argv[3]
    sleepTime = float( sys.argv[4] )

    csrfToken = getCSRFToken( event )
    while True:
        orderToken = getOrderToken( event, csrfToken, ticketId, ticketQuantity )
        if orderToken:
            break
        time.sleep( sleepTime )
    time.sleep( 1 )
    orderId = getOrderId( orderToken )

    print( f"[+] Success: https://kktix.com/events/{ event }/registrations/{ orderId }" )

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e
        print( f"[-] Error: { e }" )
