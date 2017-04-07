#!/usr/bin/env python2

from __future__ import print_function

# import sys
import argparse
import ast
import json
from HydraLib.PluginLib import connection

# sys.path.append('lib')
# TODO update class path on remote with HydraLib files


class Connector:
    def __init__(self, url=None, username=None, password=None, port=None):

        if url is None or username is None:
            return

        self.url = url
        self.username = username
        self.password = password
        self.port = port

        self.conn = connection.JsonConnection(url)

        data = self.conn.login(username, password)
        self.session_id = self.conn.sessionid

    def retrieve_projects(self, user=None):

        projects = self.conn.call('get_projects', {'user_id': user})
        print(projects)
        return projects

    def retrieve_networks(self, project=None):

        if project is None:
            print("Must provide project id to retrieve list of network ids")
            return

        networks = self.conn.call('get_networks', {'project_id': project})
        print(networks)
        return networks

    def retrieve_network(self, network=None):

        if network is None:
            print("Must provide network id to retrieve a specific network")
            return

        network = self.conn.call('get_network', {'network_id': network})
        print(network)
        return network


def debug_print(var_name, var_value=None):

    print(var_name + ": ", end="")
    print(var_value) if var_value is not None else print("None")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', dest='debug', action='store_const', const=True,
                        help='if option is used will print debug statements')

    parser.add_argument('-n', '--network', dest='net', type=int, help='network id number - integer')

    parser.add_argument('-s', '--password', dest='pw', type=str, help='usernames password')

    parser.add_argument('-p', '--port', dest='port', type=int, help='port number - integer')

    parser.add_argument('-j', '--project', dest='proj', type=int, help='project id number - integer')

    parser.add_argument('-r', '--url', dest='url', type=str, help='IP address or name')

    parser.add_argument('-u', '--username', dest='un', type=str, help='Hydra users name')

    parser.add_argument('-l', '--local', dest='local', action='store_const', const=True,
                        help='if option is used will use local data file instead of querying server')

    args = parser.parse_args()

    if args.debug is True:

        for i in args.__dict__:
            debug_print(i, args.__dict__[i]) if args.__dict__[i] is not None else debug_print(i)

    connector = Connector(args.url, args.un, args.pw)

    # projects = hc.retrieve_projects()
    # print("\ntype of 'projects'" + type(projects).__name__ + "\n")
    #
    # if type(projects) is list:
    #     print("it's a list")
    #
    # networks = hc.retrieve_networks(args.proj)
    # print("\ntype of 'networks'" + type(networks).__name__ + "\n")
    #
    # if type(networks) is list:
    #     print("it's a list")

    network = connector.retrieve_network(args.net)
    print("\ntype of 'network'" + type(network).__name__ + "\n")

    if type(network) is connection.JSONObject:
        print("it's a JSONObject")
        network_dict = ast.literal_eval(json.dumps(network))

        print(network_dict)
        print("\ntype of 'network_dict'" + type(network_dict).__name__ + "\n")





