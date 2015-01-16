# Template to base deployment WSGI scripts on
# Edit these paths to match the deployment environment

VIRTUALENV_PATH = "/path/to/env/"
PROJECT_PATH = "/path/to/app/"

# Set up app environment

activate_this = VIRTUALENV_PATH + 'bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, PROJECT_PATH)

from sankarit import app as application