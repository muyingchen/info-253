#!/bin/bash
export FLASK_APP=webserver.py
export INFO253_MAILGUN_USER="api"
export INFO253_MAILGUN_PASSWORD="key-dfae0c4b134d68419e282e3de269a426"
export INFO253_MAILGUN_DOMAIN="sandboxf62fba07abaf4227a1682571c51b86c9.mailgun.org"
flask run
