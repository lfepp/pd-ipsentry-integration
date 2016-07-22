#!/usr/bin/python

"""This applet captures an alert output from IPSentry and delivers the alert \
to PagerDuty.
"""

import argparse
import hashlib
import json
import os.path
import requests

__author__ = 'Nick McLarty <nick@tamu.edu>'
__copyright__ = '2014 Texas A&M Transportation Institute'
__license__ = 'GPL v3'
__version__ = '1.1'

# Set variables/constants
url = "https://events.pagerduty.com/generic/2010-04-15/create_event.json"

# Capture arguments
parser = argparse.ArgumentParser(description='This applet captures an alert output from IPSentry and delivers \
the alert to PagerDuty.')
parser.add_argument('-k', '--key', help='PagerDuty API Service Key',
                    required=True)
parser.add_argument('-s', '--status',
                    help='Status of service (OK or CRITICAL)', required=True)
parser.add_argument('-n', '--name', help='Name of service', required=True)
parser.add_argument('-a', '--addr', help='Address of service', required=True)
parser.add_argument('-c', '--client', help='Name of client', required=False)
parser.add_argument('-u', '--url', help='URL of client', required=False)
parser.add_argument('--details', help='Result details', required=False)
parser.add_argument('--notes', help='Alert notes', required=False)
args = parser.parse_args()

# Read in incident keys file or makes a new one if it does not exist
if os.path.isfile('incident_keys.json'):
    with open('incident_keys.json', 'r') as data_file:
        incident_keys = json.load(data_file)
else:
    incident_keys = {}
    with open('incident_keys.json', 'w') as data_file:
        data_file.write(json.dumps(incident_keys))

# Find incident key for ongoing or resolved incidents
service_hash = hashlib.md5(args.name.encode('utf-8')).hexdigest()
try:
    incident_keys[service_hash]
    incident_key = incident_keys[service_hash]
except:
    incident_key = None

# Determine if this is a new, ongoing, or resolved incident
if args.status == 'OK':
    event_type = 'resolve'
else:
    event_type = 'trigger'

# Show values
print("Service Key: %s" % args.key)
print("Status: %s" % args.status)
print("Name: %s" % args.name)
print("Address: %s" % args.addr)
print("Client: %s" % args.client)
print("URL: %s" % args.url)
print("Details: %s" % args.details)
print("Notes: %s" % args.notes)
print("Service Hash: %s" % service_hash)
print("Incident Key: %s" % incident_key)

# Build payload for HTTP request to PagerDuty
payload = {
    'service_key': args.key,
    'event_type': event_type,
    'description': args.name,
    'client': args.client,
    'client_url': args.url,
    'details': {
    }
}
if incident_key:
    payload['incident_key'] = incident_key
if args.addr:
    payload['details']['address'] = args.addr
if args.details:
    payload['details']['details'] = args.details
if args.notes:
    payload['details']['notes'] = args.notes

# Send payload to PagerDuty and output response
r = requests.post(url, data=json.dumps(payload))
response = json.loads(r.text)
print("Response from PagerDuty API: %s" % response)

# Write new incident key file
if args.status == 'CRITICAL':
    if not incident_key:
        incident_keys[service_hash] = response['incident_key']
elif args.status == 'OK':
    del incident_keys[service_hash]
with open('incident_keys.json', 'w') as data_file:
    data_file.write(json.dumps(incident_keys))
