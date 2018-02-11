import requests
import logging
import textwrap
from bs4 import BeautifulSoup


class Way2sms(object):
    URL = 'http://www.way2sms.com'

    def __init__(self):
        self.base_url = requests.head(Way2sms.URL, allow_redirects=True).url  # url after redirect

        self.session = requests.session()
        self.token = ''

    def login(self, username, password):
        self.session.headers.update({'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                                     'Upgrade-Insecure-Requests': '1',
                                     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                                     'Content-Type': 'application/x-www-form-urlencoded',
                                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                     'DNT': '1', 'Accept-Encoding': 'gzip, deflate',
                                     'Accept-Language': 'en-US,en;q=0.8'})

        payload = {'username': username, 'password': password}
        _login_url = '/'.join([self.base_url, 'Login1.action?'])

        _login = self.session.post(_login_url, data=payload)

        if _login.ok:
            self.token = self.session.cookies['JSESSIONID']
            self.token = self.token[4:]
            print('Successfully logged in.')
            # here we can also store this token in a file
        else:
            print('Login failed')

    def logout(self):
        _logout_url = '/'.join([self.base_url, 'main.action'])
        self.session.get(_logout_url)
        self.token = ''
        self.session.close()
        print('Logged out')

    def send(self, to_number, message):

        if not self.token:
            print('Not logged in')
            return

        _send_sms_url = '/'.join([self.base_url, 'smstoss.action'])

        url_safe_message = message.strip()

        message_list = textwrap.wrap(url_safe_message, 140)

        for i, message in enumerate(message_list):
            message_length = len(message)

            payload = {'ssaction': 'ss',
                       'Token': self.token,
                       'mobile': to_number,
                       'message': message,
                       'msgLen': str(140 - message_length)
                       }

            resp = self.session.post(_send_sms_url, data=payload)

            quota_finished_text = "Rejected : Can't submit your message, finished your day quota."

            if len(message_list) > 1:
                print('Part [{}/{}]'.format(i + 1, len(message_list)), end=' ')

            if quota_finished_text not in resp.text:
                print('Successfully sent.')
            else:
                print('Not sent, Quota finished.')

    def send_later(self):
        raise NotImplemented

    def check_quota(self):
        raise NotImplemented
