#!/usr/bin/env python

import time
import yaml
import logging
import argparse
import threading

from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.executions import Execution

# Global Variables
endpoint_dict = {}
blueprint_id = ''
deployments_list = []
errors_list = []
deployments_count = 0
max_threads = 0
currently_executing = 0
current_workflows_count = 0
current_deployment = 0


def current_milli_time():
    return int(round(time.time() * 1000))


def _parse_command():
    parser = \
        argparse.ArgumentParser(description='Cloudify Manager Benchmark Tool')
    parser.add_argument('--config-path', dest='config_path',
                        action='store', type=str,
                        required=True,
                        help='Configuration for Manager and Rest Server')
    parser.add_argument('--blueprint-name', dest='blueprint_id',
                        action='store', type=str,
                        required=True,
                        help='Blueprint name that will be used to create '
                             'and install deployments')
    parser.add_argument('--deployments-count', dest='deployments_count',
                        action='store', type=int,
                        required=True,
                        help='Number of Deployments to Create and install')
    parser.add_argument('--max-threads-count', dest='max_threads',
                        action='store', type=int,
                        required=True,
                        help='Maximum concurrent workflows executing')
    return parser.parse_args()


def get_workflow_status(client, deployment_id):
    status = Execution.TERMINATED
    executions = client.executions.list(deployment_id, _include=['status'])
    for execution in executions:
        if execution['status'] in (Execution.STARTED, Execution.PENDING):
            status = execution['status']
            break
        else:
            status = Execution.TERMINATED
            return status


def increment_executions(lock):
    global deployments_count
    global currently_executing
    lock.acquire()
    deployments_count = deployments_count - 1
    currently_executing = currently_executing + 1
    lock.release()


def decrement_executions(client, deployment_id, lock):
    global currently_executing
    while get_workflow_status(client, deployment_id) != Execution.TERMINATED:
        time.sleep(2)
        lock.acquire()
        currently_executing = currently_executing - 1
        lock.release()


def decrement_executions_error(lock):
    global currently_executing
    lock.acquire()
    currently_executing = currently_executing - 1
    lock.release()


def create_run_deployment(client, endpoint_dict, lock):
    global current_deployment
    global deployments_list
    global deployments_count
    global max_threads
    global currently_executing
    while deployments_count > 0:
        while currently_executing == max_threads:
            time.sleep(0.1)
        try:
            increment_executions(lock)
            deployment_id = blueprint_id + '-DT-' + str(current_milli_time()) \
                + '-' + threading.current_thread().name
            logging.info(
                'time start for deployment {0} is {1}'.format(
                    deployment_id, str(time.strftime('%Y/%m/%d %H:%M:%S'))))
            client.deployments.create(blueprint_id, deployment_id,
                                      endpoint_dict)
            while get_workflow_status(client, deployment_id) != 'terminated':
                time.sleep(2)
            try:
                client.executions.start(deployment_id, 'install')
            except Exception as ex:
                decrement_executions_error(lock)
                logging.info(
                    "error happned for deployment {0} exception {1}".format(
                        deployment_id, str(ex)))

            else:
                deployments_list.append(deployment_id)
                decrement_executions(client, deployment_id, lock)
                logging.info(
                    'time finish for successful deployment {0} is {1}'.format(
                        deployment_id, str(time.strftime('%Y/%m/%d %H:%M:%S')))
                    )
        except Exception as ex:
            decrement_executions_error(lock)
            logging.info(
                "error happned for deployment {0} exception {1}".format(
                    deployment_id, str(ex)))


def create_threads(threads, client, endpoint_dict, lock, workflow):
    x = threading.Thread(
            target=create_run_deployment,
            args=(client, endpoint_dict, lock, workflow))
    threads.append(x)
    x.start()


def destroy_threads(threads, lock):
    global deployments_count
    executionDone = False

    while not executionDone:
        lock.acquire()
        executionDone = (deployments_count == 0)
        lock.release()
        time.sleep(1)

    threads = [t for t in threads if t.is_alive()]
    for index, thread in enumerate(threads):
        thread.join()


if __name__ == '__main__':
    global blueprint_id
    parse_args = _parse_command()
    with open(parse_args.config_path) as config_file:
        config = yaml.load(config_file, yaml.Loader)
    # rest_client to cloudify manager
    client = CloudifyClient(
        host=config['manager_ip'], username=config['manager_username'],
        password=config['manager_password'], tenant=config['manager_tenant'])
    # rest server endpoint configuration
    endpoint_dict["rest_endpoint"] = config['rest_server']
    endpoint_dict["rest_endpoint_port"] = config['rest_server_port']

    deployments_count = parse_args.deployments_count
    max_threads = parse_args.max_threads
    blueprint_id = parse_args.blueprint_id

    logging.basicConfig(level=logging.INFO)
    logging.info(
        'Process start: {0}'.format(str(time.strftime('%Y/%m/%d %H:%M:%S'))))

    threads = []
    lock = threading.Lock()
    logging.info("Max Threads {0}".format(max_threads))
    for i in range(max_threads):
        create_threads(threads, client, endpoint_dict, lock)

    destroy_threads(threads, lock)
    time.sleep(1)
    logging.info("Deployments List Legnth {0}".format(len(deployments_list)))
    logging.info("Errors List Legnth {0}".format(len(errors_list)))
    logging.info(
        'Process end: {0}'.format(str(time.strftime('%Y/%m/%d %H:%M:%S'))))
