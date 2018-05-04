# WE CONNECT API [![Build Status](https://travis-ci.org/murageden/we-connect-v1.svg?branch=develop)](https://travis-ci.org/murageden/we-connect-v1) [![Coverage Status](https://coveralls.io/repos/github/murageden/we-connect-v1/badge.svg?branch=develop)](https://coveralls.io/github/murageden/we-connect-v1?branch=develop) [![CircleCI](https://circleci.com/gh/murageden/we-connect-v1/tree/develop.svg?style=svg)](https://circleci.com/gh/murageden/we-connect-v1/tree/develop) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6ada5fc7ae404ba4a34df38000943f94)](https://www.codacy.com/app/murageden/we-connect-v1?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=murageden/we-connect-v1&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/e9a7fe6947609eabe6a2/maintainability)](https://codeclimate.com/github/murageden/we-connect-v1/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/e9a7fe6947609eabe6a2/test_coverage)](https://codeclimate.com/github/murageden/we-connect-v1/test_coverage)

## About
WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with. This app is live on https://weconn.herokuapp.com/


## Documentation
See full documentation [here](https://weconnnect.docs.apiary.io/)


## Installation
### Required
* Git: [Installing Git on Linux, Mac OS X and Windows](https://gist.github.com/derhuerst/1b15ff4652a867391f03)
* Python 3.*: [Python Download and Installation Instructions](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html)
* Pip: [Python & pip Windows installation](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)
* Virtualenv: [Installation — virtualenv 15.1.0 documentation](https://virtualenv.pypa.io/en/stable/installation/)


### Initialize a Local Repository
Run `git init` on a terminal


### Clone This Repository
Run `git clone https://github.com/murageden/we-connect-v1.git`
Run `cd we-connect-v1/`


### Set up Virtual Environment
Run the following code on a Windows terminal:

```bash
virtualenv --python=python3 venv
source venv/Scripts/activate
```
or if on Linux/Unix terminal:

```bash
virtualenv --python=python3 venv
source venv/bin/activate
```


### Install Requirements
Run `pip install -r requirements.txt`


### Run the API on Localhost
```bash
export FLASK_APP=api/__init__.py
flask run
```


The API has the following endpoints working:

* Users Endpoints:

Method | Endpoint URL | Description
--- | --- | ---
`POST` | `/api/v1/auth/register` | Creates a new user account
`POST` | `/api/v1/auth/login` | Logs in a user
`POST` | `/api/v1/auth/logout` | Logs out a user
`POST` | `/api/v1/auth/reset-password` | Resets a user password

* Businesses Endpoints:

Method | Endpoint URL | Description
--- | --- | ---
`POST` | `/api/v1/businesses` | Registers a business
`PUT` | `/api/v1/businesses/<businessId>` | Modify a business profile
`DELETE` | `/api/v1/businesses/<businessId>` | Deletes a business profile
`GET` | `/api/v1/businesses` | Retrieve a list of all registered businesses
`GET` | `/api/v1/businesses/<businessId>` | Retrieve a single business with this id

* Reviews Endpoints:

Method | Endpoint URL | Description
--- | --- | ---
`POST` | `/api/v1/businesses/<businessId>/reviews` | Create a review for a business
`GET` | `/api/v1/businesses/<businessId>/reviews` | Retrieve reviews for a business with this id

