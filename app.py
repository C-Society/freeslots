# -*- coding:utf8 -*-
# !/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
import time
import pandas as pd
import datetime
from datetime import timedelta
import string
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import os
import json

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "FreeSlot":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("name")
    now = datetime.datetime.now()
    now = now + timedelta(hours=5, minutes=30)
    Day = datetime.datetime.today().weekday()
    # Because we have holiday on weekends :-p
    Day = 3
    if Day < 5:
        # Convert time in 12 hour format
        if now.hour in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 4, 3]:
            if now.hour > 12:
                time = now.hour % 12
            # The CSV file
            df = pd.read_csv("Free_Slot.csv")

            df1 = df.loc[df['Day'] == Day]
            df2 = df1.loc[:, name]
            df3 = df2.loc[df['Time'] == time]
            df4 = df3.values
            res = makeWebhookResult2(df4[0], name)
        else:
            res = makeWebhookResult3(name)
    else:
        res = makeWebhookResult(name)
    return res

def makeWebhookResult(name):
    # print(json.dumps(item, indent=4))
    speech = name + " is free because today is holiday. Dumb!!!"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-freeslot-webhook-sample"
    }

def makeWebhookResult2(data,name):
    # print(json.dumps(item, indent=4))
    if data == "free":
        speech = name + " is " + data + " right now!!"
    else:
        speech = name + " is in " + data + " right now!!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-freeslot-webhook-sample"
    }

def makeWebhookResult3(name):
    # print(json.dumps(item, indent=4))
    speech = name + " is free because classes are over. Dumb!!!"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-freeslot-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
