#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: HydraData Project: api
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import configparser
import requests
import json

from src.HydrologicData import HydrologicData

config = configparser.ConfigParser()
config.read('conf/hydra.conf')


def _build_url(host, port, scheme, path):
    scheme = scheme if scheme else config['HYDRA']['scheme']
    host = host if host else config['HYDRA']['host']
    port = port if port else config['HYDRA']['port']
    path = path if path else config.get('HYDRA', 'path')

    return "%s://%s:%s/%s" % (scheme, host, port, path)


class HydraData(HydrologicData):

    def __init__(self, username=None, password=None, host=None, port=None, scheme=None, path=None):
        self.username = username if username else config['HYDRA']['username']
        self.password = password if password else config['HYDRA']['password']

        self.url = _build_url(host, port, scheme, path)
        # self.url = url if url else config['HYDRA']['url']
        # self.port = port if port else config['HYDRA']['port']
        self.app_name = 'dawuap-webapi'
        self.session_id = self._login()

    def _login(self):
        login_params = {
            'username': self.username,
            'password': self.password,
        }

        try:
            response = self._call('login', login_params)
            return response.get('sessionid')
        except Exception as ex:
            print('made it')

    def _retrieve_network(self, network_id):
        print('here')
        return "getnet"

    def _retrieve_networks(self):
        pass

    def _retrieve_projects(self):
        pass

    def _call(self, func, args):
        call = {func: args}
        headers = {
            'Content-Type': 'application/json',
            'sessionid': self.session_id if hasattr(self, 'session_id') else None,
            'appname': self.app_name,
        }

        response = requests.post(self.url, data=json.dumps(call), headers=headers)

        # todo - everyone likes clean error handling
        if not response.ok:
            raise Exception

        response_json = json.loads(response.content)

        return response_json
