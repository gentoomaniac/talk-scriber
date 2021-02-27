#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Sample Script
    Version 0.2.1
"""

import logging
import sys

import click


log = logging.getLogger(__file__)


def _configure_logging(verbosity):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3', 'google.auth.transport.requests':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)


@click.group()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    """ main program
    """
    _configure_logging(verbosity)

    log.info('I am an informational log entry in the sample script.')
    return 0


@cli.command(name='foo')
def foobar():
    print("bar")


if __name__ == '__main__':
    # pylint: disable=E1120
    sys.exit(cli())
