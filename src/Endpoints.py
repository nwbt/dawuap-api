#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# 
# File: Endpoints Project: api
# Copyright © 2017 Dan Catalano <dev@nwbt.co>
#
# Distributed under terms of the MIT license.
import cherrypy

from src.HydraData import HydraData

@cherrypy.expose
class DawuapWebService(object):

    @cherrypy.expose # get network
    @cherrypy.tools.json_out()
    def network(self, network_id=0):
        if network_id < 1:
            cherrypy.response.status = '404'
            return

        cherrypy.response.status = '200'

        hydraData = HydraData()
        val = hydraData.get_network(network_id)
        return(val)

if __name__ == '__main__':
    cherrypy.tree.mount(DawuapWebService(), '/', 'conf/dawuap.conf')
    cherrypy.config.update("conf/dawuap.conf")
    cherrypy.engine.start()
    cherrypy.engine.block()
