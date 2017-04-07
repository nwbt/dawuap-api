#!/usr/bin/env python2

import argparse

import geojson
import pyproj


class HydraNetworkDTO:
    def __init__(self, network_dict: dict):
        self.__network_dict = network_dict  # save for future use
        self.__links = self.__network_dict['links']
        self.__nodes = self.__network_dict['nodes']

    def build_geojson(self) -> geojson.FeatureCollection:
        nodes = self.__nodes
        links = self.__links

        feature_list = []

        _build_node_feature_list(feature_list, nodes)
        _build_link_feature_list(feature_list, links)

        feature_collection = geojson.FeatureCollection(feature_list)
        return feature_collection


def _build_link_feature_list(feature_links_list, links):
    for l in links:
        coordinates = l['layout']['geometry']['coordinates']
        lines = []

        for c in coordinates:  # linestrings are comprised of multiple line segments, hence inner loop
            # todo if c len is not 2 then throw exception
            long, lat = _convertCoordinates(c[0], c[1])
            lines.append((long, lat))

        linestring = geojson.LineString(tuple(lines))
        feature_link = geojson.Feature(geometry=linestring, properties={'id': l['id'], 'name': l['name']})
        feature_links_list.append(feature_link)


def _build_node_feature_list(feature_nodes_list, nodes):
    for n in nodes:
        long, lat = _convertCoordinates(float(n['x']), float(n['y']))
        point = geojson.Point((long, lat))
        feature_node = geojson.Feature(geometry=point, properties={'id': n['id'], 'name': n['name']})
        feature_nodes_list.append(feature_node)


def _convertCoordinates(xCoord: float, yCoord: float):
    src_projection = 'EPSG:5070'
    src_pyproj = pyproj.Proj(init=src_projection)
    dest_pyproj = pyproj.Proj(proj='longlat', ellps='WGS84', datum='WGS84')

    long, lat = pyproj.transform(src_pyproj, dest_pyproj, xCoord, yCoord)
    return long, lat


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', dest='input', type=str, help='read file containing JSONObject dict in str format')
    parser.add_argument('-o', dest='output', type=str, help='write geojson contents to file')


    args = parser.parse_args()

    if args.input is not None:
        # todo check path exists
        f = open(args.input, 'r')
        hydra_network = f.read()
        hydra_networkDTO = HydraNetworkDTO(eval(hydra_network))
        fc = hydra_networkDTO.build_geojson()
        dump = geojson.dumps(fc)

        print(dump)

    if args.output is not None:
        # todo check path & dump exists
        f = open(args.output, 'w')
        f.write(dump)
        f.close()
