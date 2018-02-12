# -*- coding:utf8 -*-
# !/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
import time
import pandas as pd
import datetime
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
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "FreeSlot":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("name")
    name = str.lower(name)
    # The CSV file
    df = pd.read_csv("Free_Slot.csv")
    df_check = df.loc[df['Day'] == 21]
    df_check = df_check.values
    if name in df_check:
        now = datetime.datetime.now()
        Day = datetime.datetime.today().weekday()
        # Because we have holiday on weekends :-p



        if Day < 5:
            working_hour = [8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19]
            if now.hour in working_hour:
            # Convert time in 12 hour format
                if now.hour > 12:
                    time = now.hour % 12

                df1 = df.loc[df['Day'] == Day]
                data = "test test"
                res = makeWebhookResult3(data)
                return res
         
                df2 = df1.loc[:, name]
                df3 = df2.loc[df['Time'] == time]
                df4 = df3.values
                res = makeWebhookResult2(df4[0], name)
            else:
                res = makeWebhookResult3(name)
        else:
            res = makeWebhookResult(name)
        return res
    else:
        return {}
            

def makeWebhookResult(name1):
    # print(json.dumps(item, indent=4))
    speech = name1 + " is free because today is holiday. Dumb!!!"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-freeslot-webhook-sample"
    }

def makeWebhookResult2(data2,name2):
    # print(json.dumps(item, indent=4))
    if data2 == "free":
        speech = name2 + " is " + data2 + " right now!!"
    else:
        speech = name2 + " is in " + data2 + " right now!!"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "dialogflow-freeslot-webhook-sample"
    }

def makeWebhookResult3(name3):
    # print(json.dumps(item, indent=4))
    speech = name3 + " is free because classes are over. Dumb!!!"
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
