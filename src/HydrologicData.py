#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: HydrologicData Project: api
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.


class HydrologicData(object):

    def get_network(self, network_id):
        return self._retrieve_network(network_id)

    def _retrieve_network(self, network_id):
        assert False, 'retrieve_network must be defined!'

    def get_networks(self):
        return self._retrieve_networks()

    def _retrieve_networks(self):
        assert False, 'retrieve_networks must be defined!'

    def get_projects(self):
        return self._retrieve_projects()

    def _retrieve_projects(self):
        assert False, 'retrieve_projects must be defined!'
