#! /usr/bin/env python

"""
pyroute.

Usage:
  pyroute route <table_file> <address_file>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
from ipaddress import ip_network, ip_address
import os


def parse_table(table_file):
    table_dict = {}
    with open(table_file) as table_file_handle:
        for line in table_file_handle.readlines():
            asid, subnet, cost = line.strip().split()
            if not asid in table_dict: table_dict[asid] = {ip_network(subnet, False) : cost}
            else: table_dict[asid][ip_network(subnet, False)] = cost
    return table_dict

def parse_address_file(address_file):
    with open(address_file) as address_file_handle:
        return [ip_address(line.strip()) for line in address_file_handle.readlines()]

def route_address(table, address):
    routes = {}
    for asid, subnets_dict in table.items():
        for subnet, cost in subnets_dict.items():
            if not address in subnet: break
            if not address in routes or cost < list(routes[address].values())[0]:
                routes[address] = {asid: cost}
    return routes

def route(table, addresses):
    for address in addresses:
        route_dict = route_address(table, address)
        if not route_dict:
            print(address, 'X')
        else:
            asdict = route_dict[address]
            print(address, list(asdict.keys())[0])

def main(usage):
    table_dict = parse_table(usage['<table_file>'])
    addresses = parse_address_file(usage['<address_file>'])
    route(table_dict, addresses)

if __name__ == '__main__':
    main(docopt(__doc__))
