# -*- coding: utf-8 -*-

# Copyright © 2012 Humbug, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import simplejson
import requests
import time
import traceback
import urlparse
import sys
import os
import optparse
from distutils.version import LooseVersion
from ConfigParser import SafeConfigParser
import logging
import client


__version__ = "0.1.6"
Client = client.Client

# Check that we have a recent enough version
# Older versions don't provide the 'json' attribute on responses.
assert(LooseVersion(requests.__version__) >= LooseVersion('0.12.1'))

def generate_option_group(parser):
    group = optparse.OptionGroup(parser, 'API configuration')
    group.add_option('--site',
                      default=None,
                      help=optparse.SUPPRESS_HELP)
    group.add_option('--api-key',
                     action='store')
    group.add_option('--user',
                     dest='email',
                     help='Email address of the calling user.')
    group.add_option('--config-file',
                     action='store',
                     help='Location of an ini file containing the above information.')
    group.add_option('-v', '--verbose',
                     action='store_true',
                     help='Provide detailed output.')

    return group

def init_from_options(options):
    return Client(email=options.email, api_key=options.api_key, config_file=options.config_file,
                  verbose=options.verbose, site=options.site)


def _mk_subs(streams):
    return {'subscriptions': streams}

def _mk_rm_subs(streams):
    return {'delete': streams}

def _mk_events(event_types=None):
    if event_types is None:
        return dict()
    return dict(event_types=event_types)

Client._register('send_message', url='messages', make_request=(lambda request: request))
Client._register('get_messages', method='GET', url='messages/latest', longpolling=True)
