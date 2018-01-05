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
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'default.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(object):
    DEBUG = False


class DebugConfig(object):
    DEBUG = True


