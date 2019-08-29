import random
import re

import requests
from decouple import config


def handle_error(send):
    prog = re.compile(r'<status>(.*?)</status>')
    status_code = int(prog.findall(send.text)[0])
    try:
        if status_code != 0:
            raise ValueError
        else:
            print('Успешно доставлено')
    except ValueError:
        print(f'Message not sent. Response code {status_code}')


def send_sms(phone, message=''):
    headers = {'Content-Type': 'application/xml'}

    xml = '''
        <message>
                <login>''' + config('NIKITA_SMS_LOGIN') + '''</login>
                <pwd>''' + config('NIKITA_SMS_PASSWORD') + '''</pwd>
                <id>''' + str(random.randrange(1, 1000)) + '''</id>
                <sender>''' + config('NIKITA_SMS_SENDER') + '''</sender>
                <text>''' + str(message) + '''</text>
                <phones>
                    <phone>''' + str(phone) + '''</phone>
                </phones>
            </message>    
    
    '''
    xml = xml.encode('utf-8')

    send = requests.post('https://smspro.nikita.kg/api/message', data=xml, headers=headers)

    return handle_error(send)

