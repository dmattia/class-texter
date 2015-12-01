#!/usr/bin/python

import logging
import sys
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/flask/class_text")

from routes import app as application
application.secret_key = os.environ.get('TEXTING_SECRET_KEY', '')
