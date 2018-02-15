import os
from way2sms import Way2sms


MOBILE_NO = os.getenv('MOBILE_NO')
PASS = os.getenv('PASS')
TO_MOBILE_NO = os.getenv('TO_MOBILE_NO')
MSG = os.getenv('MSG')


w2s = Way2sms()

w2s.login(MOBILE_NO, PASS)

w2s.send(TO_MOBILE_NO, MSG)

w2s.logout()
