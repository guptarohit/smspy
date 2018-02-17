from __future__ import print_function

import requests
import datetime
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

        payload = {
            'username': username,
            'password': password
        }
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
        print('Successfully logged out')

    def send(self, to_number, message):

        if not self.token:
            print('Not logged in')
            return

        _send_sms_url = '/'.join([self.base_url, 'smstoss.action'])

        url_safe_message = message.strip()

        message_list = textwrap.wrap(url_safe_message, 140)

        for i, message in enumerate(message_list):
            message_length = len(message)

            payload = {
                'ssaction': 'ss',
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
                if self._sent_verify(to_number, message):
                    print('Successfully sent.')
                else:
                    print('Failed to send.')
            else:
                print('Not sent, Quota finished.')

    def _sent_verify(self, mobile, message):
        print('Verifying sent message.')
        if not self.token:
            print('Not logged in')
            return

        today = datetime.date.today().strftime('%d/%m/%Y')

        payload = {
            'Token': self.token,
            'dt': today
        }

        _sent_verify_url = '/'.join([self.base_url, 'sentSMS.action'])

        resp = self.session.post(_sent_verify_url, data=payload)

        soup = BeautifulSoup(resp.text, 'html.parser')

        first = soup.find('div', {'class': 'mess'})
        _mobile = str(first.find('b').text)
        divrb = first.find('div', {'class': 'rb'})
        _message = str(divrb.find('p').text)
        if _mobile == str(mobile) and _message == message:
            return True
        else:
            return False

    def schedule(self, mobile, message, date, time):
        if not self.token:
            print('Not logged in')
            return

        _schedule_url = '/'.join([self.base_url, 'schedulesms.action'])

        _date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')
        _time = datetime.datetime.strptime(time, '%H:%M').strftime('%H:%M')

        url_safe_message = message.strip()

        message_list = textwrap.wrap(url_safe_message, 140)

        quota_finished_text = "Rejected : Can't submit your message, finished your day quota."

        for i, message in enumerate(message_list):
            message_length = len(message)

            payload = {
                'Token': self.token,
                'mobile': mobile,
                'sdate': _date,
                'stime': _time,
                'message': message,
                'msgLen': str(140 - message_length)
            }

            resp = self.session.post(_schedule_url, data=payload)

            if len(message_list) > 1:
                print('Part [{}/{}]'.format(i + 1, len(message_list)), end=' ')

            if quota_finished_text not in resp.text:
                if self._schedule_verify(mobile, message, date, time):
                    print('Successfully scheduled, on {} {}'.format(_date, _time))
                else:
                    print('Unable to schedule message.')
            else:
                print('Not sent, Quota finished.')

    def _schedule_verify(self, mobile, message, date, time):
        print('Verifying scheduled message.')
        if not self.token:
            print('Not logged in')
            return

        _date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
        _time = datetime.datetime.strptime(time, '%H:%M').strftime('%I:%M %p')

        timestamp = '{} {}'.format(_time, _date)

        payload = {
            'Token': self.token,
            'dt': _date
        }

        _sent_verify_url = '/'.join([self.base_url, 'MyfutureSMS.action'])

        resp = self.session.post(_sent_verify_url, data=payload)

        soup = BeautifulSoup(resp.text, 'html.parser')

        msgs_lst = []
        msgs = soup.findAll('div', {'class': 'mess'})

        for msg in msgs:
            _mobile = str(msg.find('a').text)
            divrb = msg.find('div', {'class': 'rb'})
            _message = divrb.find('p').text
            original_message = '\n'.join(_message.splitlines()[1:-2])
            divbot = msg.find('div', {'class': 'bot'})
            _time = divbot.find('p', {'class': 'time'}).text

            msgs_lst.append([_mobile, original_message, _time])

        if [str(mobile), message, timestamp] in msgs_lst:
            return True
        else:
            return False

    def scheduled_messages(self, date):
        if not self.token:
            print('Not logged in.')
            return

        _date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

        payload = {'Token': self.token, 'dt': _date}

        _scheduled_messages_url = '/'.join([self.base_url, 'MyfutureSMS.action'])

        resp = self.session.post(_scheduled_messages_url, data=payload)

        soup = BeautifulSoup(resp.text, 'html.parser')

        part = soup.find_all('div', {'class': 'mess'})

        headers = ['Time', 'Mobile no', 'SMS', 'Original SMS']
        data = []

        for div in part:
            t = div.find('p', {'class': 'time'})
            time = t.find('span').text
            mobile_no = div.find('a').text
            divrb = div.find('div', {'class': 'rb'})
            message = divrb.find('p').text
            original_message = '\n'.join(message.splitlines()[1:-2])
            data.append([time, mobile_no, message, original_message])

        return headers, data

    def history(self, date):
        if not self.token:
            print('Not logged in')
            return

        _date = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d/%m/%Y')

        payload = {'Token': self.token, 'dt': _date}

        _history_url = '/'.join([self.base_url, 'sentSMS.action'])

        resp = self.session.post(_history_url, data=payload)

        soup = BeautifulSoup(resp.text, 'html.parser')

        part = soup.find_all('div', {'class': 'mess'})

        headers = ['Time', 'Mobile no', 'SMS']
        data = []

        for div in part:
            t = div.find('p', {'class': 'time'})
            time = t.find('span').text
            mobile_no = div.find('b').text
            divrb = div.find('div', {'class': 'rb'})
            message = divrb.find('p').text
            data.append([time, mobile_no, message])

        return headers, data

    def quota_left(self):
        if not self.token:
            print('Not logged in')
            return

        today = datetime.date.today().strftime('%d/%m/%Y')

        payload = {
            'Token': self.token,
            'dt': today
        }

        _quota_left_url = '/'.join([self.base_url, 'sentSMS.action'])

        resp = self.session.post(_quota_left_url, data=payload)

        soup = BeautifulSoup(resp.text, 'html.parser')

        sms_sent = len(soup.find_all('div', {'class': 'mess'}))
        sms_left = 100 - sms_sent

        print('You have {} sms left for today.'.format(sms_left))
        return sms_left
