#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zach <zacharyzjp@gmail.com>
#
# Distributed under terms of the MIT license.
import os
import unittest
from uimgmt.models import DockerMachine as dm
from uimgmt.models import MacVlanInterface as mvi
from uimgmt.models import Label

"""
Unit tests for uimgmt
"""
CODE_200_OK = '200 OK'
CODE_404_NFD = '404 NOT FOUND'
LBL_NONE = list() 
LBL_1 = [{'name': 'label_4_test', 'desc': 'this is the decription of the label'}]
MACHINES = (
        {
        'hostname' : 'machine_4_test_1',
        'ip_addr' : '10.11.59.183',
        'intfs' : 'enp3s2',
        'labels' : LBL_1
        },
        {
        'hostname': 'machine_4_test_2',
        'ip_addr': '124.100.2.1',
        'intfs': 'intf4test',
        'labels' : LBL_NONE 
        },
        )

class UimgmtTestCase(unittest.TestCase):
    #Variables for Test input
    txt_success_add_machine = 'Add new machine successfully!'
    txt_invalid_ip_add = 'Invalid IP address'
    txt_invalid_hostname = 'field is required'

    intf_data = dict(name='test_intf_name', machine_id=6, subnet='124.124.0.0/24',
            min_vlan=100, max_vlan=200)

    @classmethod
    def setUpClass(cls):
       pass


    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        print('Doing setUp')
        from uimgmt import app, db
        self.app = app
        self.db = db
        self.app.testing =True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.test_client = app.test_client()
        self.dbseed()


    def tearDown(self):
        print('Doing tearDown')
        #self.delete_all_machines()
        #self.delete_all_interface()
        #self.delete_all_labels()
        #self.db.session.commit()
        machines = dm.query.all()
        if machines:
            for m in machines:
                intfs = m.interfaces.all()
                if intfs:
                    for intf in intfs: 
                        intf.labels.clear()
                m.labels.clear()
                self.db.session.delete(m)
        self.delete_all_labels()
        self.db.session.commit()


    def dbseed(self):
        self.machines = []
        for m in MACHINES:
            machine = dm(hostname=m['hostname'], ip_addr=m['ip_addr'])
            if m['intfs']:
                for intf in m['intfs'].split(' '):
                    self.db.session.add(mvi(name=intf, machine=machine))
            if m['labels']:
                for lbl in m['labels']:
                    machine.mark(Label(name=lbl['name'], desc=lbl['desc']))
            self.machines.append(machine)
            self.db.session.add(machine)
            self.db.session.commit()


    def delete_all_machines(self):
        dm.query.delete()


    def delete_all_interface(self):
        mvi.query.delete()


    def delete_all_labels(self):
        Label.query.delete()

    def test_get_home(self):
        resp = self.test_client.get('/')
        self.assertEqual(resp.status, "200 OK")


    def test_get_machine(self):
        print('test get machine') 
        resp = self.test_client.get('/machine/')
        self.assertEqual(resp.status, CODE_200_OK)
        txt_content = resp.data.decode()

        for m in MACHINES:
            self.assertIn(m['hostname'], txt_content)
            self.assertIn(m['ip_addr'], txt_content)
            if m['intfs']:
                for intf in m['intfs'].split(' '):
                    self.assertIn(intf, txt_content)
            if m['labels']:
                for lbl in m['labels']:
                    self.assertIn(lbl['name'], txt_content)
                    self.assertIn(lbl['desc'], txt_content)


    def test_add_machine(self):
        m_data = dict(hostname='test_machine_hostname', ip_addr='124.124.0.1')
        resp = self.test_client.post('/machine/add',
                data=m_data,
                follow_redirects=True)
        self.assertEqual(resp.status, CODE_200_OK)
        txt_content = resp.data.decode()
        self.assertIn(m_data.get('hostname'), txt_content)
        self.assertIn(UimgmtTestCase.txt_success_add_machine, txt_content) 


    def test_add_machine_with_invalid_ip(self):
        m_invalid_ip_addr = dict(
                hostname='machine_with_invalid_ip',
                ip_addr='10.0.0.1.2'
                )
        resp = self.test_client.post('/machine/add',
                data=m_invalid_ip_addr,
                follow_redirects=True)
        self.assertEqual(resp.status, CODE_200_OK)
        assert UimgmtTestCase.txt_invalid_ip_add in resp.data.decode()


    def test_del_machine(self):
        m_item = dm.query.first()
        resp = self.test_client.open('/machine/del/{}'.format(m_item.id),
                follow_redirects=True)
        self.assertEqual(resp.status, CODE_200_OK)
        assert m_item.hostname.encode() not in resp.data


    def test_del_machine_nonexist(self):
        resp = self.test_client.open('/machine/del/10000', follow_redirects=True)
        self.assertEqual(resp.status, CODE_200_OK)


    def test_del_machine_unexpected_id(self):
        resp = self.test_client.open('/machine/del/id_not_integer',
                follow_redirects=True)
        self.assertEqual(resp.status, CODE_404_NFD)


    def test_get_interface(self):
        resp = self.test_client.get('/interface/')
        self.assertEqual(resp.status, "200 OK")


    def test_add_interface(self):
        m_id = dm.query.first().id
        intf_data = dict(
                name='test_intf_name',
                machine_id=m_id, subnet='124.124.0.0/24',
                min_vlan=100, max_vlan=200
                )
        resp = self.test_client.post('/interface/add',
                data=intf_data,
                follow_redirects=True)
        self.assertEqual(resp.status, CODE_200_OK)
        assert intf_data.get('name').encode() in resp.data


if __name__ == '__main__':
    unittest.main()
