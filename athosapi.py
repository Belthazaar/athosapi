#!/usr/bin/env python3

import argparse
import json
from flask import Flask, request, jsonify
from flask.wrappers import Response
from shelljob import proc

app = Flask(__name__)

athos_dir = ""

@app.route('/push_config', methods=['PUT'])
def push_config():
    """"Stores the topology config within athos directory """
    with open(f"{athos_dir}/etc/athos/topology.json", "w+") as f:
        json.dump(request.json, f, indent=2)
    temp = None
    t = None
    with open(f"{athos_dir}/etc/athos/topology.json", "r") as f:
        temp = f.read()
        t = json.loads(temp)
    return jsonify(t)


@app.route('/save_faucet', methods=['PUT'])
def save_faucet():
    """Stores the faucet config within athos directory """
    with open(f"{athos_dir}/etc/faucet/faucet.yaml", "w+") as f:
        f.write(request.data.decode('utf-8'))

    with open(f"{athos_dir}/etc/faucet/faucet.yaml", "r") as f:
        return Response(f.read(), mimetype='text/plain')


@app.route('/save_xml', methods=['PUT'])
def save_xml():
    """Stores the xml config within athos directory """
    with open(f"{athos_dir}/etc/athos/graph.xml", "w+") as f:
        f.write(request.data.decode('utf-8'))

    with open(f"{athos_dir}/etc/athos/graph.xml", "r") as f:
        return Response(f.read(), mimetype='text/plain')



@app.route('/test_config', methods=['PUT'])
def test_config():
    """Sotres the topology json within athos and starts a testing instance """
    with open(f"{athos_dir}/etc/athos/topology.json", "w+") as f:
        json.dump(request.json, f, indent=2)

    g = proc.Group()
    p = g.run( [ "bash", f"{athos_dir}/runDocker.sh" ] )

    def read_stdout():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return Response(read_stdout(), mimetype='text/plain')


@app.route('/run_athos', methods=['GET'])
def run_athos():
    """Starts the athos docker instance and reports the results"""
    g = proc.Group()
    p = g.run( [ "bash", f"{athos_dir}/runDocker.sh" ] )

    def read_stdout():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return Response(read_stdout(), mimetype='text/plain')


@app.route('/get_topology', methods=['GET'])
def get_topology():
    """Retrieves the topology json config that was used in Athos """
    with open(f"{athos_dir}/etc/athos/topology.json", "r") as f:
        temp = f.read()
        t = json.loads(temp)
        return jsonify(t)


@app.route('/get_xml', methods=['GET'])
def get_xml():
    """Retrieves the xml config that was used in Athos """
    with open(f"{athos_dir}/etc/athos/graph.xml", "r") as f:

        return Response(f.read(), mimetype='text/plain')




@app.route('/get_logs', methods=['GET'])
def get_logs():
    """Retrieves the logs from the athos docker instance """
    with open(f"{athos_dir}/ixpman_files/output.txt", "r") as f:

        return Response(f.read(), mimetype='text/plain')


def parse_args():
    parser = argparse.ArgumentParser(description='Athos API')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Hostname or IP address')
    parser.add_argument('--port', type=int, default=8989,
                        help='Port number')
    parser.add_argument('-athos-dir', type=str, default='/athos',
                        help='Path to athos directory')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    athos_dir = args.athos_dir
    app.run(host=args.host, port=args.port)
