#!/usr/bin/env python

import json
import argparse
import os
import socket

# Cloudera Manager passes alerts to this script as a path to a file containing JSON with the alert data
parser = argparse.ArgumentParser(description="Processes Cloudera Manager alerts in JSON file.")
parser.add_argument('alertFile', metavar='<file name>', type=file, nargs=1)

args = parser.parse_args()

# parse the JSON containing the alerts -- there could be multiple
alertList = json.load(args.alertFile[0])

# Slack has a REST interface to submit messages -- using this requires enabling "webhooks" for a channel, and this will provide a "token" that must be on the URL to the REST service
slackToken='insert_your_token_here'

# proxy definition
os.putenv("http_proxy", "http://proxy.internal:8080")
os.putenv("https_proxy", "http://proxy.internal:8080")

# loop through the alerts in the JSON and send each separately to Slack. Note that stdout goes to the cloudera manager log(s).
for alert in alertList:
    print '==============================='
    alert = alert.get('body').get('alert').get('content').replace("'", "\\u0027")
    hostname = socket.gethostname()
    formatted = ("{}: {}".format(hostname, alert))
    curlCmdPre = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"" + formatted + "\"}' https://hooks.slack.com/services/"
    curlCmd = curlCmdPre + slackToken
    print '+++++++++++++++++++++++++++++++++++'
    os.system(curlCmd)
