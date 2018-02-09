#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.
import os

"""
Define Configurations for kinds of environment
"""

base_dir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'sqlite:///' + os.path.join(base_dir, 'default.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'just a sceret key'

class ProdConfig(object):
    DEBUG = False


class DebugConfig(object):
    DEBUG = True


