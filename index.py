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
import re

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

# input validation of cron time format 
# https://gist.github.com/harshithjv/c58f0dfce0656cf94c8c
def validateCron(cronEntry):
    cron = cronEntry.split(" ")[0:5]
    cron[0] = cron[0].lstrip("#")
    validate_crontab_time_format_regex = re.compile(\
        "{0}\s+{1}\s+{2}\s+{3}\s+{4}".format(\
            "(?P<minute>\*|[0-5]?\d)",\
            "(?P<hour>\*|[01]?\d|2[0-3])",\
            "(?P<day>\*|0?[1-9]|[12]\d|3[01])",\
            "(?P<month>\*|0?[1-9]|1[012])",\
            "(?P<day_of_week>\*|[0-6](\-[0-6])?)"\
        ) # end of str.format()
    ) # end of re.compile()
    if validate_crontab_time_format_regex.match(" ".join(cron)) == None:
        return(False)
    else:
        return(True)


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
            #for line in data:
            #    if validateCron(line):
            #        continue
            #    else:
            #        return(json.dumps({'ERROR':"Wrong cron format: "+line}), 400, {'ContentType':'application/json'})
            with open(cronDir+targetFile,"wb") as fo:
                for line in reversed(data):
                    fo.write(line+"\n")
        return(json.dumps({'success':True}), 200, {'ContentType':'application/json'})
    else:
        return(json.dumps({'ERROR':"Writing file."}), 400, {'ContentType':'application/json'})
