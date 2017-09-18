from flask import Flask, request
from flask import render_template
from flask_jsglue import JSGlue
import ConfigParser
import os
import json

app = Flask(__name__)
app.debug=True
jsglue = JSGlue(app)

config = ConfigParser.ConfigParser()
config.read('crontab.cfg')
cronDir = config.get('cron', 'directory')
cronPrefix = config.get('cron', 'prefix')

@app.route('/')
def hello_world():
    return 'Hello, World113!'


@app.route('/crontab')
def read_cron():
    crons = {}
    try:
	for cronfile in os.listdir(cronDir):
	    if cronfile.endswith(cronPrefix):
		with open(os.path.join("/etc/cron.d",cronfile)) as f:
		    crons[cronfile] = f.readlines()
        return render_template("crontab.html", lines=crons)
    except IOError:
        pass
    return "Unable to read file"

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
	return(json.dumps({'success':False}), 1, {'ContentType':'application/json'})
