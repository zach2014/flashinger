#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.

from uimgmt import app, db
from uimgmt.models import Label, DockerMachine, MacVlanInterface

"""
Application main entrypoint
"""
@app.shell_context_processor
def enter_shell_context():
    return {'db': db, 'Label': Label, 'DockerMachine': DockerMachine, 'MacVlanInterface': MacVlanInterface}


def add_and_commit(entry):
    db.session.add(entry)
    db.session.commit()

db.save = add_and_commit

dummy_label = Label(name='dummy_lbl', desc='This is a dummy label')
demo_label = Label(name='demo1_lbl', desc='This is the 1st demo label')
demo_label1 = Label(name='demo2_lbl', desc='This is the 2nd demo label')

dummy_node1 = DockerMachine(hostname='dummy_node1', ip_addr='192.168.1.1')
dummy_node2 = DockerMachine(hostname='dummy_node2', ip_addr='192.168.1.2')
demo_node = DockerMachine(hostname='demo_node', ip_addr='10.11.59.183')
demo_node1= DockerMachine(hostname='demo_node1', ip_addr='10.11.59.171')
dummy_node1.mark(dummy_label)
dummy_node2.mark(dummy_label)
demo_node.mark(demo_label)
demo_node.mark(demo_label1)
demo_node1.mark(demo_label)
demo_node1.mark(demo_label1)
# add duplicated label
demo_node.mark(demo_label)

machines = [dummy_node1, dummy_node2, demo_node, demo_node1]

dummy_intf1 = MacVlanInterface(name='eth1', machine=dummy_node1)
dummy_intf2 = MacVlanInterface(name='eth2', machine=dummy_node2)
demo_intf = MacVlanInterface(name='enp3s2', machine=demo_node)
demo_intf1 = MacVlanInterface(name='eth-no-existed', machine=demo_node)
demo_intf2 = MacVlanInterface(name='enp3s0', machine=demo_node1)
demo_intf3 = MacVlanInterface(name='eth-no-existed', machine=demo_node1)
dummy_intf1.mark(dummy_label)
dummy_intf2.mark(dummy_label)
demo_intf.mark(demo_label)
demo_intf1.mark(demo_label1)
demo_intf2.mark(demo_label)
demo_intf3.mark(demo_label1)
# mark duplicated label
dummy_intf1.mark(dummy_label)
demo_intf.mark(demo_label)
v_intfs = [dummy_intf1, dummy_intf2, demo_intf, demo_intf1, demo_intf2, demo_intf3]


@app.cli.command('dbseed')
def dbseed_command():
    """ doing db seed for testing in development"""
    for  m in machines:
        db.session.add(m)
    for v in v_intfs:
        db.session.add(v)
    db.session.commit()

    print('dbseed done.')

@app.cli.command('dbclean')
def dbclean_command():
    """doing db clean after testing in development"""
    db.drop_all()
    print('dbclean done')
