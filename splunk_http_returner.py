# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Import python libs
import json
import logging

# Import Salt libs
import salt.utils.jid
import salt.returners

# Import third party libs
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

log = logging.getLogger(__name__)

# Define virtual name
__virtualname__ = 'splunk_http'


def __virtual__():
    if not HAS_REQUESTS:
        return False
    return __virtualname__


def _get_options(ret=None):
    attrs = {'url': 'url',
             'token': 'token'}
    _options = salt.returners.get_returner_options('returner.{0}'.format
                                                   (__virtualname__),
                                                   ret,
                                                   attrs,
                                                   __salt__=__salt__,
                                                   __opts__=__opts__)
    return _options


def _return_states(data, url, token):
    if data.get('fun') == 'state.sls' or data.get('fun') == 'state.highstate':
        log.info('{0}: Sending event_return to url "{1}"'.format(__virtualname__, url))
        log.debug('{0}: {1}'.format(__virtualname__, data))
        for state_name, state in data.get('return').iteritems():
            # Add extra data to state event
            state.update({'state_name': state_name,
                          'state_id': state_name.split('_|-')[1],
                          'minion_id': data.get('id'),
                          'jid': data.get('jid'),
                          'fun': data.get('fun')})
            event = {'event': state}
            requests.post(
                url,
                headers={'Authorization': 'Splunk {0}'.format(token)},
                data=json.dumps(event),
                verify=False
            )


def event_return(events):
    _options = _get_options()
    url = _options.get('url')
    token = _options.get('token')
    for event in events:
        data = event.get('data', {})
        _return_states(data, url, token)
