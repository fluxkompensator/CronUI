CronUI
======

CronUI is an web-based tool based on Python Flask, jquery and bootstrap to view, edit, delete and create cron jobs.
![alt text](https://raw.githubusercontent.com/fluxkompensator/CronUI/master/cronUI.png)

## Features

* list cron jobs
* modify cron jobs
* delete cron jobs
* create cron jobs

## Requirements

* Python
* Flask
* Flask-JSGlue

* All used Crontabs (defined by prefix in crontab.cfg) 
* This program must be run as root

## Installation

```
pip install Flask
pip install Flask-JSGlue

git clone https://github.com/fluxkompensator/CronUI.git

cd CronUI
export FLASK_APP=index.py
```
edit the file crontab.cfg to your needs with your favorite editor, `vim`, `nano`, ...
```
export FLASK_DEBUG=0
export FLASK_APP="index.py"
sudo -E python -m flask run --host=0.0.0.0
```

> App will now run public on port 5000.
> All set up. Running in privileged mode.
> Serving Flask app "index"
> Forcing debug mode on
> Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

## License

Apache License 2.0.
