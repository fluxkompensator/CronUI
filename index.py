#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    index.py
    ~~~~~~~~~
    Modified default flask app called Flask.
    :license: Apache License 2.0, see LICENSE for more details.
"""

from flask import Flask, request, render_template
from flask_jsglue import JSGlue
#from croniter import croniter
import ConfigParser
import json
import os

# start app, inject modules
app = Flask(__name__)
jsglue = JSGlue(app)

# check if being executed with root privileges | terminate if not root
if os.geteuid() == 0:
    print("All set up. Running in privileged mode.")
else:
    print("This program needs to be run as root.")
    print("Example: export FLASK_APP='index.py'; sudo -E python -m flask run --host=0.0.0.0")
    exit(1)

# Settings
config = ConfigParser.ConfigParser()
config.read('crontab.cfg')
cronDir = config.get('cron', 'directory')
cronPrefix = config.get('cron', 'prefix')

# read in cron files to dict
def readcron():
    crons = {}
    try:
        for cronfile in os.listdir(cronDir):
            if cronfile.endswith(cronPrefix):
                with open(os.path.join("/etc/cron.d",cronfile)) as f:
                    crons[cronfile] = f.readlines()
        return crons
    except IOError:
        pass
    return "Unable to read file"

# temp function for input validation
def validateCron(cronEntry):
    print(cronEntry)
    pass

# root site 
@app.route('/')
def default():
    crons = readcron()
    return render_template("crontab.html", lines=crons)

# crontab site
@app.route('/crontab')
def crontab():
    crons = readcron()
    return render_template("crontab.html", lines=crons)

# writes cron files on POST
@app.route('/crontabsave', methods=['POST'])
def crontabsave():
    if request.method == 'POST':
        data = json.loads(request.data)
        targetFile = data.pop()
        app.logger.info('%s', targetFile)
        for i in data:
            app.logger.info('%s', i)
            with open(cronDir+targetFile,"wb") as fo:
                for line in reversed(data):
                    fo.write(line+"\n")
        return(json.dumps({'success':True}), 200, {'ContentType':'application/json'})
    else:
        return(json.dumps({'success':False}), 400, {'ContentType':'application/json'})
