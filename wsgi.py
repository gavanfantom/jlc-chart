#!/usr/bin/env python3

import sys
from os import path

sys.path.insert(0, path.abspath(path.dirname(__file__)))

from jlcchart import create_app
application = create_app()
