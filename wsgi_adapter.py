#-*- coding: utf-8 -*-
import sys,os

import logging
from systemd.journal import JournalHandler
# logging config
log_formatter = "[%(module)s:%(levelname)s]%(message)s"
# log to journald
logging.basicConfig(level=logging.DEBUG, handlers=[JournalHandler()], format=log_formatter)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

#debug
logging.debug("wsgi adapter loaded.")

from doorlocker_main import app as application

