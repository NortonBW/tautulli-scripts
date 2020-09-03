
'''
Run script by itself. Will toggle the Alternative Speed mode in qBitTorrent at
times when Plex is streaming non-local content. 
'''

import requests
import argparse
import sys
import datetime

## EDIT THESE SETTINGS ##
QBITTORRENT_API_URL = 'http://192.168.1.200:8082/api/v2/'
QBITTORRENT_API_USERNAME = 'admin'
QBITTORRENT_API_PASSWORD = 'adminadmin'

def toggleSpeedLimitsMode(session):
    """
    Toggles the state of Alternative Download mode
    """
    r = session.get(QBITTORRENT_API_URL + "transfer/toggleSpeedLimitsMode")
    return r.text

def main():
    sys.stdout = open('log.txt', 'w')

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', '-a', type=str, help='START or STOP')
    parser.add_argument('--streams', '-s', type=int, help='Stream count')
    args = parser.parse_args()

    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    print(timestamp, "Action=", args.action, "Streams=", str(args.streams))

    #Start session
    s = requests.Session()

    #authenticate/login
    r = s.get(QBITTORRENT_API_URL + 'auth/login' +
        '?username='+ QBITTORRENT_API_USERNAME +
        '&password=' + QBITTORRENT_API_PASSWORD)


    #get current speed limit mode
    r = s.get(QBITTORRENT_API_URL + "transfer/speedLimitsMode")
    if r.status_code == 200:
        speedLimited = bool(int(r.text))

    #check conditions and determine if the mode needs to be toggled
    if args.streams == 0 and speedLimited == True:
        toggleSpeedLimitsMode(s)
    elif args.streams > 0 and speedLimited == False:
        toggleSpeedLimitsMode(s)

    sys.stdout.close()


if __name__ == "__main__":
    main()
