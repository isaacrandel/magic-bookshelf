
import json
import signal
from termcolor import (
    colored,
    cprint,
)
import time
import urlparse

import espeak
from pirc522 import RFID
import requests

run = True
rdr = RFID.RFID()
util = rdr.util()
util.debug = True

API_ROOT = 'http://localhost:5000/'
API_BOOK = API_ROOT + 'book/?uid='
API_CHECKIN = API_ROOT + 'checkin/'
API_CHECKOUT = API_ROOT + 'checkout/'


def banner(text, ch='=', length=78):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    return banner

def end_read(signal,frame):
    global run
    print ("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print(banner('Magic Bookshelf RFID Controller'))
print('Waiting for books...')

curr_uid = None

es = espeak.ESpeak()

while run:
    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))
    (error, uid) = rdr.anticoll()
    if not error:
        suid = '-'.join(str(seg) for seg in uid)
        print("Card read UID: %s" % suid)
        #if curr_uid != suid and suid != None:
        print('New card detected: %s' % suid)
        retrieve_url = API_BOOK + suid
        print('Getting book from: %s' % retrieve_url)
        response = requests.get(retrieve_url)

        if response.status_code != 200:
            print('Error getting book with UID %s' % suid)
        else:
            book = json.loads(response.text)
            print('Got book: %s' % book['title'])
            book = json.loads(response.text)
            if book['checkedin'] == 0:
                checkin_url = urlparse.urljoin(API_CHECKIN, suid)
                requests.get(checkin_url)
                cprint(colored('Checked-in: %s' % book['title']), 'green')
                es.say('Checked in %s by %s' % (book['title'], book['author']))
            else:
                checkout_url = urlparse.urljoin(API_CHECKOUT, suid)
                requests.get(checkout_url)
                cprint(colored('Checked-out: %s' % book['title']), 'red')
                es.say('Checked out %s by %s' % (book['title'], book['author']))
            curr_uid = suid

        util.set_tag(uid)
        #util.auth(rdr.auth_a, [0x12, 0x34, 0x56, 0x78, 0x96, 0x92])
        util.auth(rdr.auth_b, [0x74, 0x00, 0x52, 0x35, 0x00, 0xFF])
        util.read_out(4)
        util.deauth()

        time.sleep(1)
