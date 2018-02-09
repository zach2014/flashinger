#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.
from flask_wtf import  FlaskForm
from wtforms import StringField,IntegerField, SelectMultipleField, validators
from wtforms.validators import ValidationError
from uimgmt.models import DockerMachine

"""
Forms to post data
"""
def validate_hostname_exist(form, field):
    if DockerMachine.query.filter_by(hostname=field.data).count() > 0 :
        raise ValidationError('hostname already exist')


def validate_ipaddr_exist(form, field):
    if DockerMachine.query.filter_by(ip_addr=field.data).count() > 0:
        raise ValidationError('ip address already exist')

class MachineForm(FlaskForm):
    hostname = StringField('HostName', validators=[validators.required(), validate_hostname_exist])
    ip_addr = StringField('IP Address', validators=[validators.required(), validators.IPAddress(), validate_ipaddr_exist])
    #labels = SelectMultipleField('Labels')

class InterfaceForm(FlaskForm):
    name = StringField('Name', validators=[validators.required()])
    machine_id = IntegerField('Machine', validators=[validators.required()])
    subnet = StringField('Subnet', validators=[validators.required()])
    min_vlan = IntegerField('Min_Vlan', validators=[validators.required()])
    max_vlan = IntegerField('Max_Vlan', validators=[validators.required()])
    #labels = SelectMultipleField('Lables')


class UpgraderServiceForm(FlaskForm):
    c_name = StringField('Name')
    vlan_id = IntegerField('Vlan')
    fw_oid = StringField('Firmware')
    intf_id = IntegerField('Interface')
