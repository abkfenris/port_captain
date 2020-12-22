#!/usr/bin/env python
"""
Run port_captain from the command line to validate and sync configs
"""
import argparse
import pathlib
import sys
from typing import List, Iterator

from pydantic import ValidationError

from port_captain.logger import logger
from port_captain.platform import Thing


class Arguments(argparse.Namespace):
    files: List[pathlib.Path]
    dir: List[pathlib.Path]

    dynamo: bool

    def all_files(self) -> Iterator[pathlib.Path]:
        """ Return all the files selected or found in directories """
        if self.files:
            for file in self.files:
                yield file

        if self.dir:
            for dir in self.dir:
                for file in dir.glob("**/*.yaml"):
                    yield file

        return


def parse_args(args: List[str]) -> Arguments:
    """ Parse input arguments """
    parser = argparse.ArgumentParser(
        "port_captain",
        description="Validate selected files and directories to check that they generate valid configurations for IOOS Cloud Ingress. Optionally configs can be synced to DynamoDB",
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="files",
        action="append",
        type=pathlib.Path,
        help="Files to validate",
    )
    parser.add_argument(
        "-d",
        "--dir",
        action="append",
        type=pathlib.Path,
        help="Directories to validate yaml files in",
    )
    parser.add_argument(
        "--dynamo",
        action="store_true",
        help="Sync configurations to DynamoDB after successful validation",
    )

    arguments = Arguments()

    parsed_args = parser.parse_args(args, namespace=arguments)

    if not (parsed_args.files or parsed_args.dir):
        parser.error("No files specified, add --file or --dir")

    return parsed_args


def main(args: List[str] = None):
    if not args:
        args = sys.argv[1:]
    arguments = parse_args(args)

    all_files_valid = True
    things: List[Thing] = []

    # validate files
    for path in arguments.all_files():
        try:
            thing = Thing.parse_yaml(path)
        except ValidationError as e:
            all_files_valid = False
            indented_error = "\n".join(["  " + line for line in str(e).splitlines()])
            logger.error(f"Error validating {path}: \n  {indented_error}")
        else:
            logger.info(f"{path} is valid YAML")
            things.append(thing)

    if arguments.dynamo and not all_files_valid:
        logger.warning("Skipping syncing data to dynamo due to validation error")

    # if valid and dynamo sync data to dynamodb
    if all_files_valid and arguments.dynamo:
        logger.info("Syncing to DynamoDB")


if __name__ == "__main__":
    main(sys.argv[1:])
