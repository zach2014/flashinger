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
machines_labels = db.Table('machines_labels',
        db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True),
        db.Column('machine_id', db.Integer, db.ForeignKey('docker_machine.id'), primary_key=True)
    )


interfaces_labels = db.Table('interfaces_labels',
        db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key=True),
        db.Column('interface_id', db.Integer, db.ForeignKey('macvlan_interface.id'), primary_key=True)
    )


class Label(db.Model):
    """Schema of label for marking resource"""
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.String(256), nullable=False)


class DockerMachine(db.Model):
    """Schema of docker machines"""
    __tablename__ = 'docker_machine'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64))
    ip_addr =  db.Column(db.String(15), nullable=False, unique=True)
    interfaces = db.relationship('MacVlanInterface', backref='machine', lazy='dynamic')
    labels = db.relationship('Label', secondary=machines_labels, lazy='subquery', 
            backref=db.backref('machines', lazy=True))


    def __repr__(self):
        if self.hostname :
            return  '<{} hostname {}, ip_addr {} >'.format(self.__class__.__name__,
                    self.hostname,
                    self.ip_addr)
        else:
            return  '<{} ip_addr {} >'.format(self.__class__.__name__, self.ip_addr)


    def mark(self, label):
        if not self.is_marked(label):
            self.labels.append(label)
            return self


    def unmark(self, label):
        if self.is_marked(label):
            self.labels.remove(user)
            return self


    def is_marked(self, label):
        return self.labels.count(label) > 0


class MacVlanInterface(db.Model):
    """Schema of macvlan interface"""
    __tablename__ = 'macvlan_interface'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey('docker_machine.id'), nullable=False)
    subnet = db.Column(db.String(18), nullable=False, default='192.168.0.1/24')
    min_vlan = db.Column(db.Integer, nullable=False, default=1)
    max_vlan = db.Column(db.Integer, nullable=False, default=4094 )
    labels = db.relationship('Label', secondary=interfaces_labels, lazy='subquery',
            backref=db.backref('interfaces', lazy=True)) 


    def mark(self, label):
        if not self.is_marked(label):
            self.labels.append(label)
            return self


    def unmark(self, label):
        if self.is_marked(label):
            self.labels.remove(label)
            return self


    def is_marked(self, label):
        return self.labels.count(label) >0


