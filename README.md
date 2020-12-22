# port_captain

Captain of the Port (also known as a harbormaster or `port_captain`) is a tool
to help manage 'things' (buoy/glider/datalogger/...) sending data to the IOOS Cloud Sensor Ingest project and where that data goes next.

It also has command line functionality to validate thing configs, and sync those configs to DynamoDB.

## Installation

### Development

For local development install with `pip install -e .`

## Command line usage

The most common usage of Captain of the Port will be via the command line, where it can be used to validate configurations of different things.

With a valid config:

```sh
➜ port_captain -f tests/example_configs/A01.yaml
INFO - tests/example_configs/A01.yaml is valid YAML
```

And an invalid one:

```sh
➜ port_captain -f tests/example_configs/A01.yaml
ERROR - Error validating tests/example_configs/A01.yaml:
    1 validation error for Thing
  platform -> maintainer -> email
    value is not a valid email address (type=value_error.email)
```


```sh
usage: port_captain [-h] [-f FILES] [-d DIR] [--dynamo]

Validate selected files and directories to check that they generate valid
configurations for IOOS Cloud Ingress. Optionally configs can be synced to
DynamoDB

optional arguments:
  -h, --help            show this help message and exit
  -f FILES, --file FILES
                        Files to validate
  -d DIR, --dir DIR     Directories to validate yaml files in
  --dynamo              Sync configurations to DynamoDB after successful
                        validation
```

## Lambda

Captain of the Port is setup as as a AWS Lambda function directing traffic within IOOS's Cloud Ingress AWS IoT Core MQTT system.
The Lambda takes incoming data based on the topic string, and will redirect it based on the configs in a repo defining which things are communicating with IoT Core.
This allows platform managers to change up data processing from their platforms without having to change settings on the deployed platforms themselves.

## Github Actions on this repo

On this repo, on every commit tests are run, and when a new commit is pushed to the `main` branch,
the lambda is updated.

## Github Actions on other repos

Captain of the Port is designed to use by another repo of things sending data to IOOS Cloud Ingress.
When a PR is submitted to the repo, `port_captain` is run to make sure all configs are valid.
Additionally when the PR is merged to the `main` branch, the configs are synced to DynamoDB, and a new 'thing' is added to AWS IoT Core.