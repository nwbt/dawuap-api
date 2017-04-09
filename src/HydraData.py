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
import geojson
import pyproj

from src.HydrologicData import HydrologicData

config = configparser.ConfigParser()
config.read('conf/hydra.conf')


def _build_url(host, port, scheme, path):
    scheme = scheme if scheme else config['HYDRA']['scheme']
    host = host if host else config['HYDRA']['host']
    port = port if port else config['HYDRA']['port']
    path = path if path else config.get('HYDRA', 'path')

    return "%s://%s:%s/%s" % (scheme, host, port, path)


def _build_feature_list_links(feature_list, links, projection):
    for link in links:
        coordinates = link.get('layout').get('geometry').get('coordinates')
        lines = []

        for coordinate in coordinates:

            if projection:
                # double parens for append to take only one value
                lines.append((_convert_coordinates(coordinate[0], coordinate[1], projection)))
            else:
                # double parens for append to take only one value
                lines.append((coordinate[0], coordinate[1]))

        line_string = geojson.LineString(tuple(lines))
        feature_link = geojson.Feature(geometry=line_string, properties={
            'id': link.get('id', ''),
            'name': link.get('name', ''),
        })
        feature_list.append(feature_link)


def _build_feature_list_nodes(feature_list, nodes, projection):
    for node in nodes:
        x_coord = node.get('x')
        y_coord = node.get('y')

        if projection:
            point = geojson.Point((_convert_coordinates(x_coord, y_coord, projection)))
        else:
            point = geojson.Point((float(x_coord), float(y_coord)))

        feature_node = geojson.Feature(geometry=point, properties={
            'id': node.get('id', ''),
            'name': node.get('name', '')
        })
        feature_list.append(feature_node)


def _convert_coordinates(x_coord, y_coord, src_projection):
    src = pyproj.Proj(init=src_projection)
    # dst = pyproj.Proj(init='EPSG:4326')
    dst = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')
    return pyproj.transform(src, dst, x_coord, y_coord)


def _convert_to_geojson(network):
    nodes = network.get('nodes')
    links = network.get('links')
    projection = network.get('projection', '')

    feature_list = []

    _build_feature_list_links(feature_list, links, projection)
    _build_feature_list_nodes(feature_list, nodes, projection)

    feature_collection = geojson.FeatureCollection(feature_list)

    print(geojson.is_valid(feature_collection))
    return feature_collection


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

    def _retrieve_network(self, network_id, is_geojson):
        if not type(network_id) is int:
            network_id = int(network_id)
        network = self._call('get_network', {'network_id': network_id})

        if is_geojson:
            network = _convert_to_geojson(network)

        return network

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
