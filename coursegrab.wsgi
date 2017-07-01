#!/usr/bin/python
activate = '/var/www/CourseGrab/env/bin/activate_this.py'
execfile(activate, dict(__file__=activate))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/CourseGrab/")

from runserver import application
application.secret_key = 'Add your secret key'
