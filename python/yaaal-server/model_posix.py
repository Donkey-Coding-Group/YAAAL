#!/usr/bin/python
# coding: utf-8
# author: Niklas Rosenstein <rosensteinniklas@googlemail.com>

import os
import sys
import json

# Thank God that modules are saved in sys.modules, otherwise this would lead to
# an infinite recursion (as this file is imported by `model`).
import model



