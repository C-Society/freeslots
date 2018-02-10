# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    # Convert time in 12 hour format
    if now.hour in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
        if now.hour > 12:
            time = now.hour % 12
        # The CSV file
        df = pd.read_csv("Free_Slot.csv")
        Day = datetime.datetime.today().weekday()
        print(Day)
        # Because we have holiday on weekends :-p
        Day = 3
        if Day > 4:
            res = makeWebhookResult(name)
        else:
            df1 = df.loc[df['Day'] == Day]
            df2 = df1.loc[:, name]
            df3 = df2.loc[df['Time'] == time]
            df4 = df3.values
            res = makeWebhookResult2(df4[0], name)
    else:
        res = makeWebhookResult3(name)
    return res

def makeWebhookResult(data):
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

def makeWebhookResult3(data):
    # print(json.dumps(item, indent=4))
    speech = data + "is free because classes are over. Dumb!!!"
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
