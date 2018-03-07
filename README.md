# WE CONNECT API [![Build Status](https://travis-ci.org/murageden/bootcamp.svg?branch=Flask-API)](https://travis-ci.org/murageden/bootcamp) [![Coverage Status](https://coveralls.io/repos/github/murageden/bootcamp/badge.svg?branch=Flask-API)](https://coveralls.io/github/murageden/bootcamp?branch=Flask-API)

## About
WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with


## Documentation
See full documentation [here](https://weconnnect.docs.apiary.io/)


## Installation
### Required
* Git: [Installing Git on Linux, Mac OS X and Windows](https://gist.github.com/derhuerst/1b15ff4652a867391f03)
* Python: [Python Download and Installation Instructions](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)
* Pip: [Python & pip Windows installation](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)
* Virtualenv: [Installation — virtualenv 15.1.0 documentation](https://virtualenv.pypa.io/en/stable/installation/)


### Initialize a Local Repository
Run `git init` on a terminal


### Clone This Repository
Run `git clone https://github.com/murageden/bootcamp.git`
Run `cd bootcamp/`


### Set up Virtual Environment
Run the following code on a Windows terminal:

```bash
virtualenv venv
source venv/Scripts/activate
```
or if on Linux/Unix terminal:

```bash
virtualenv venv
source venv/bin/activate
```


### Install Requirements
Run `pip install requirements.txt`


### Run the API on Localhost
```bash
export FLASK_APP=api/v1/we_connect/routes.py
flask run
```

