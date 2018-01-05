#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.
from flask import  Flask
from flask_sqlalchemy import  SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from uimgmt import views, models
