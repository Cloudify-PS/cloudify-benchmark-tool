#!/usr/bin/env python

import yaml
import logging
import argparse

from cloudify_rest_client import CloudifyClient


def _parse_command():
    parser = \
        argparse.ArgumentParser(description='Cloudify Manager Benchmark Tool')
    parser.add_argument('--config-path', dest='config_path',
                        action='store', type=str,
                        required=True,
                        help='Configuration for Manager and Rest Server')
    parser.add_argument('--blueprint-path', dest='bp_path',
                        action='store', type=str,
                        required=True,
                        help='Blueprint path that will be uploaded to manager')
    parser.add_argument('--blueprint-name', dest='bp_name',
                        action='store', type=str,
                        required=True,
                        help='Blueprint name that will be uploaded to manager')
    return parser.parse_args()


if __name__ == '__main__':

    parse_args = _parse_command()
    with open(parse_args.config_path) as config_file:
        config = yaml.load(config_file, yaml.Loader)
    # rest_client to first manager from the cluster
    client = CloudifyClient(
        host=config['manager_ip'], username=config['manager_username'],
        password=config['manager_password'], tenant=config['manager_tenant'])

    logging.basicConfig(level=logging.INFO)

    try:
        client.blueprints.upload(parse_args.bp_path, parse_args.bp_name)
    except Exception as e:
        logging.info(
            "error happned for during the upload exception {1}".format(str(e)))
