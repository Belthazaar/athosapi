# Athos REST API

This is a small wrapper api designed to be used with athos and Miru. This allows
Miru to start the athos docker container without giving the www-data user account
access to the container itself. This wrapper simply provides RESTful API endpoints
storing and retrieving the configs used in athos, as well as the starting the
athos docker instance.

*IMPORTANT: This will need be run as root, or at least a user with docker access with NET capabilities.*

Because of this we recommend limiting connections to localhost or in an internal network only.

The default address used is `127.0.0.1:8989`

The API end points used by Miru is as follows:

| Endpoint | Method | Action |
| -------- | ------ | ------ |
| `/push_config` | `PUT` | Stores the topology json file in `{athos_dir}/etc/athos/topology.json` |
| `/save_faucet` | `PUT` | Stores the faucet config file in `{athos_dir}/etc/faucet/faucet.yaml` |
| `/save_xml` | `PUT` | Stores the mxgraph xml file in `{athos_dir}/etc/athos/graph.xml` |
| `/test_config` | `PUT` | Stores the topology json and starts the athos docker instance. Streams the cmd results back |
| `/run_athos` | `PUT` | Starts the athos docker instance. Streams the cmd results back |
| `/get_xml` | `GET` | Returns the mxgraph xml file in `{athos_dir}/etc/athos/graph.xml` |
| `/get_config` | `GET` | Returns the topology json file in `{athos_dir}/etc/athos/topology.json` |
| `/get_logs` | `GET` | Returns the logs from the last time that Athos ran |

args:

| args | description |
| ---- | ----------- |
| `--athos-dir` | The athos directory to use. Defaults to `/athos` |
| `--host` | The host to listen on. Defaults to `127.0.0.1` |
| `--port` | The port to listen on. Defaults to `8989` |
