#!/usr/bin/env python3

import urllib.request
import argparse
import getpass

def geturl(url, user, pw):
    #Cargo cult to avoid external dependencies
    req = urllib.request.Request(url)
    pwm = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    pwm.add_password(None, url, user, pw)
    auth_manager = urllib.request.HTTPBasicAuthHandler(pwm)
    opener = urllib.request.build_opener(auth_manager)
    urllib.request.install_opener(opener)
    try:
        handler = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return e.read().decode('utf-8')
        else:
            print('Unexpected error')
            raise
    return handler.read().decode('utf-8')

parser = argparse.ArgumentParser(
    description='Acquires a configuration from an OpenVPN portal.',
    epilog='Usually you should run as: ovpngc.py -U \
    https://openvpnaccess.local:443/ -u ubul -f ~/bin/vpn.conf')
parser.add_argument(
    '-u', '--user', help='Your username for the OpenVPN portal')
parser.add_argument(
    '-p', '--password', help='Your username for the OpenVPN portal')
parser.add_argument(
    '-U', '--url', help='The OpenVPN portal hostname, protocol and port')
parser.add_argument(
    '-f', '--file', help='The file to write the resulting configuration',
    default='client.ovpn')
args = parser.parse_args()

url = args.url + 'rest/GetUserlogin'

if args.password is None:
    args.password = getpass.getpass()

print('First query...')
text = geturl(url, args.user, args.password)
secret = []
for line in text.split('\n'):
    if 'CRV1:R,E' in line:
        secret = line.split(':')
number = getpass.getpass('Google number please: ')
pw = '::'.join(('CRV1', secret[2], number))
print('Second query...')
text = geturl(url, args.user, pw)
print('Writing out results to the file ', args.file)
with open(args.file, 'w') as f:
    f.write(text)
