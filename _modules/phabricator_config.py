# -*- coding: utf-8 -*-
'''
Support for phabricator configuration
'''
from __future__ import absolute_import

# Import python libs
import os

import logging
# Import salt libs
import salt.utils

log = logging.getLogger(__name__)

__virtualname__ = 'phabricator_config'


def __virtual__():
    '''
    Module load only if php is installed
    '''
    if salt.utils.which('php'):
        return __virtualname__
    else:
        return False


def _bin_dir():
    return __salt__['config.get']('phabricator:bin_dir')


def _phab_config_exec(command, bin=None):
    if bin is not None:
        if os.path.isfile(bin):
            phab_bin = bin
        else:
            phab_bin = os.path.join(bin, 'config')
    else:
        phab_bin = os.path.join(_bin_dir(), 'config')

    return '%s %s' % (phab_bin, command)


def list_options(**kwargs):
    return __salt__['cmd.run'](_phab_config_exec('list',
                                                 bin=kwargs.get('bin', None)))


def get_option(name, **kwargs):
    phab_cmd = _phab_config_exec('get', bin=kwargs.get('bin', None))

    if name is not None and len(name.strip()) > 0:
        phab_cmd = '%s %s' % (phab_cmd, name)

    # config get <option_name> returns json if it success
    cmd_json = __salt__['cmd.run'](phab_cmd)
    try:
        option_values = salt.utils.serializers.json.deserialize(cmd_json)
    except:
        log.error('Unable to parse JSON from command %s' % (phab_cmd,))

    option_value = None
    # option_values['config'] contains a local and a database option
    # local option value has priority over database one
    for scope in ['local', 'database']:
        if option_value is None:
            for t_option in option_values['config']:
                if (t_option['source'] == scope
                        and t_option['key'] == name
                        and t_option['status'] == 'set'):
                    option_value = t_option['value']
                    break
        else:
            break

    return option_value


def set_option(name, value, **kwargs):
    phab_cmd = _phab_config_exec('set', bin=kwargs.get('bin', None))

    if name is not None and len(name.strip()) > 0:
        phab_cmd = '%s %s "%s"' % (phab_cmd, name, value)

    return __salt__['cmd.run'](phab_cmd)


def delete_option(name, **kwargs):
    phab_cmd = _phab_config_exec('delete', bin=kwargs.get('bin', None))

    if name is not None and len(name.strip()) > 0:
        phab_cmd = '%s %s' % (phab_cmd, name)

    return __salt__['cmd.run'](phab_cmd)


if __name__ == "__main__":
    __salt__ = ''

    import sys
    sys.exit(0)
