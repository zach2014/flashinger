#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.

from uimgmt import db

"""
Schema of models
"""
class UpgraderNode(db.Model):
    """Schema for UpgraderNode model."""
    __tablename__ = 'upgrader_node'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    ip_addr = db.Column(db.String(15), nullable=False)
    if_name = db.Column(db.String(32), nullable=False)

    def __init__(self, name, ip_addr, if_name):
        self.name = name
        self.ip_addr = ip_addr
        self.if_name = if_name

    def __repr__(self):
        return '<name {}, ip_addr {}, if_name {} >'.format(self.name, self.ip_addr, self.if_name)


